from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views import View
from utils.send_email_tool import send_email_code
from .forms import SendEmailForm, RegisterForm, LoginForm, ResetPasswordFirstForm, ResetPasswordSecondForm, \
    ChangeAvatarForm, ChangeInfoForm
from .models import UserInfo, Member
from book.models import Book
from operation.models import Collect, Attention
from django_redis import get_redis_connection
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class RegisterView(View):
    @staticmethod
    def get(request):
        send_email_form = SendEmailForm()
        return render(request, 'register.html', {'send_email_form': send_email_form})

    @staticmethod
    def post(request):
        register_form = RegisterForm(request.POST)
        send_email_form = SendEmailForm()
        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            verify_code = register_form.cleaned_data['verify_code']
            if UserInfo.objects.filter(username=email):
                return render(request, 'register.html', {'error_msg': '用户已存在', 'send_email_form': send_email_form})
            if password1 != password2:
                return render(request, 'register.html', {'error_msg': '两次密码不一致', 'send_email_form': send_email_form})
            conn = get_redis_connection('default')
            email_key = '{}_1'.format(email)
            if conn.get(email_key) == verify_code.encode():
                conn.delete(email_key)
                user = UserInfo.objects.create_user(email, email, password1)
                login(request, user)
                return redirect(reverse('index'))
            else:
                return render(request, 'register.html', {'error_msg': '邮箱验证码错误', 'send_email_form': send_email_form})
        else:
            return render(request, 'register.html',
                          {'register_form': register_form, 'send_email_form': send_email_form})


class LoginView(View):
    @staticmethod
    def get(request):
        if 'email' in request.COOKIES:
            email = request.COOKIES.get('email')
            checked = 'checked'
        else:
            email = ''
            checked = ''
        return render(request, 'login.html', {'email': email, 'checked': checked})

    @staticmethod
    def post(request):
        login_form = LoginForm(request.POST)
        remember = request.POST.get('remember')
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                next_url = request.GET.get('next', reverse('index'))
                response = redirect(next_url)
                login(request, user)
                if remember == 'on':
                    response.set_cookie('email', email, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('email')
                return response
            else:
                return render(request, 'login.html', {'err_msg': '账号/密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class EmailVerifyCodeView(View):
    @staticmethod
    def post(request):
        send_email_form = SendEmailForm(request.POST)
        if send_email_form.is_valid():
            email = send_email_form.cleaned_data['email']
            send_type = send_email_form.cleaned_data['send_type']
            status = UserInfo.objects.filter(username=email)
            if send_type == "1":
                if status:
                    return JsonResponse({'status': 'fail', 'err_msg': '[用户已存在]'})
            else:
                if not status:
                    return JsonResponse({'status': 'fail', 'err_msg': '[用户不存在]'})
            msg = send_email_code(email, send_type)
            return JsonResponse({'status': 'ok', 'msg': msg})
        else:
            return JsonResponse({'status': 'fail', 'err_msg': send_email_form.errors})


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect(reverse('user:login'))


class ResetPasswordFirstView(View):
    @staticmethod
    def get(request):
        send_email_form = SendEmailForm()
        return render(request, 'reset_password1.html', {'send_email_form': send_email_form})

    @staticmethod
    def post(request):
        send_email_form = SendEmailForm()
        reset_password_first_form = ResetPasswordFirstForm(request.POST)
        if reset_password_first_form.is_valid():
            email = reset_password_first_form.cleaned_data['email']
            verify_code = reset_password_first_form.cleaned_data['verify_code']
            if not UserInfo.objects.filter(username=email):
                return render(request, 'reset_password1.html',
                              {'error_msg': '用户不存在', 'send_email_form': send_email_form})
            conn = get_redis_connection('default')
            email_key = '{}_2'.format(email)
            if conn.get(email_key) != verify_code.encode():
                return render(request, 'reset_password1.html',
                              {'error_msg': '邮箱验证码错误', 'send_email_form': send_email_form})
            else:
                request.session['reset_password_email'] = email
                request.session.set_expiry(300)
                return redirect(reverse('user:reset_password2'))
        else:
            return render(request, 'reset_password1.html',
                          {'reset_password_first_form': reset_password_first_form, 'send_email_form': send_email_form})


class ResetPasswordSecondView(View):
    def __init__(self, **kwargs):
        super(ResetPasswordSecondView, self).__init__(**kwargs)
        self.reset_password_email = ''

    def dispatch(self, request, *args, **kwargs):
        self.reset_password_email = request.session.get('reset_password_email', None)
        if not self.reset_password_email:
            return redirect(reverse('user:reset_password1'))
        result = super(ResetPasswordSecondView, self).dispatch(request, *args, **kwargs)
        return result

    @staticmethod
    def get(request):
        return render(request, 'reset_password2.html')

    def post(self, request):
        reset_password_second_form = ResetPasswordSecondForm(request.POST)
        if not reset_password_second_form.is_valid():
            return render(request, 'reset_password2.html', {'reset_password_second_form': reset_password_second_form})
        else:
            password1 = reset_password_second_form.cleaned_data['password1']
            password2 = reset_password_second_form.cleaned_data['password2']

            if password1 != password2:
                return render(request, 'reset_password2.html', {'error_msg': '两次密码不一致'})
            try:
                user = UserInfo.objects.get(username=self.reset_password_email)
            except UserInfo.DoesNotExist:
                return render(request, 'reset_password2.html', {'error_msg': '用户不存在'})
            user.set_password(password1)
            user.save()
            try:
                del request.session['reset_password_email']
            except KeyError:
                pass
            return redirect(reverse('user:login'))


@method_decorator(login_required, name='dispatch')
class UserInfoView(View):
    def get(self, request):
        member = Member.filter_member(request.user)
        context = {
            'title': 'center',
            'title1': 'info',
            'member': member
        }
        return render(request, 'user_center_info.html', context)

    def post(self, request):
        change_info_form = ChangeInfoForm(request.POST, instance=request.user)
        if change_info_form.is_valid():
            change_info_form.save(commit=True)
        return redirect(reverse('user:info'))


@method_decorator(login_required, name='dispatch')
class ChangeAvatarView(View):
    @staticmethod
    def post(request):
        change_avatar_form = ChangeAvatarForm(request.POST, request.FILES, instance=request.user)
        if change_avatar_form.is_valid():
            change_avatar_form.save(commit=True)
        return redirect(reverse('user:info'))


@method_decorator(login_required, name='dispatch')
class UserBookshelfView(View):
    @staticmethod
    def get(request):
        collect_list = Collect.objects.filter(collect_man=request.user)
        context = {
            'title': 'center',
            'title1': 'collect',
            'collect_list': collect_list
        }
        return render(request, 'user_center_bookshelf.html', context)


@method_decorator(login_required, name='dispatch')
class UserHistoryView(View):
    @staticmethod
    def get(request):
        conn = get_redis_connection('default')
        history_key = 'history_{}'.format(request.user.id)
        book_id_list = conn.lrange(history_key, 0, -1)
        if book_id_list:
            book_list = [Book.objects.get(id=book_id.decode()) for book_id in book_id_list]
        else:
            book_list = []
        context = {
            'title': 'center',
            'title1': 'history',
            'book_list': book_list
        }
        return render(request, 'user_center_history.html', context)


@method_decorator(login_required, name='dispatch')
class UserAttentionView(View):
    @staticmethod
    def get(request):
        attention_list = Attention.objects.filter(attention_man=request.user)
        context = {
            'title': 'center',
            'title1': 'attention',
            'attention_list': attention_list
        }
        return render(request, 'user_center_attention.html', context)
