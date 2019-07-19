from django import forms
from captcha.fields import CaptchaField
from .models import UserInfo


class SendEmailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '邮箱格式错误'
        }
    )

    send_type = forms.ChoiceField(
        choices=(
            (1, 'register'),
            (2, 'reset_password'),
            (3, 'change_email'),
        ),
        required=True
    )

    captcha = CaptchaField(
        error_messages={
            'required': '验证码不能为空',
            'invalid': '验证码错误'
        }
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '邮箱格式错误'
        }
    )

    password1 = forms.CharField(
        required=True,
        min_length=6,
        max_length=15,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少6位',
            'max_length': '密码最大15位'
        }
    )

    password2 = forms.CharField(
        required=True,
        min_length=6,
        max_length=15,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少6位',
            'max_length': '密码最大15位'
        }
    )

    verify_code = forms.CharField(
        required=True,
        min_length=8,
        max_length=8,
        error_messages={
            'required': '验证码不能为空',
            'invalid': '验证码错误'
        }
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '邮箱格式错误'
        }
    )

    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=15,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少6位',
            'max_length': '密码最大15位'
        }
    )


class ResetPasswordFirstForm(forms.Form):
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '邮箱格式错误'
        }
    )

    verify_code = forms.CharField(
        required=True,
        min_length=8,
        max_length=8,
        error_messages={
            'required': '验证码不能为空',
            'invalid': '验证码错误'
        }
    )


class ResetPasswordSecondForm(forms.Form):
    password1 = forms.CharField(
        required=True,
        min_length=6,
        max_length=15,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少6位',
            'max_length': '密码最大15位'
        }
    )

    password2 = forms.CharField(
        required=True,
        min_length=6,
        max_length=15,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少6位',
            'max_length': '密码最大15位'
        }
    )


class ChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['nickname', 'address', 'phone', 'gender']


class ChangeAvatarForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['avatar']
