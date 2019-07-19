from django.shortcuts import redirect, HttpResponse, reverse
from django.http import JsonResponse
from django.views import View
from utils.Alipay_file import alipay
import datetime
from user.models import UserInfo, Member
from .models import Order, MemberDuration
from .forms import OrderForm
from django.db.models import Q
from book_city.settings import return_url, notify_url
from datetime import datetime


class OrderView(View):
    @staticmethod
    def post(request):
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = UserInfo.objects.get(Q(email=data['email']) | Q(username=data['email']))
            trade_no = Order.generate_order_num(user.id)
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=trade_no,
                total_amount=data['price'],
                subject='阳哥书城',
                return_url=return_url,
                notify_url=notify_url
            )
            pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
            Order.objects.create(order_user=user, order_price=data['price'], trade_no=trade_no)
            return JsonResponse({'status': 'ok', 'pay_url': pay_url})
        else:
            return JsonResponse(form.errors, safe=False)


class PayView(View):
    @staticmethod
    def get(request):
        """同步回调"""
        data = {}
        for key, value in request.GET.items():
            data[key] = value
        signature = data.pop("sign", None)
        if alipay.verify(data, signature):
            order_num = data.get('out_trade_no', None)
            trade_no = data.get('trade_no', None)
            order_status = 'TRADE_FINISHED'

            order = Order.objects.filter(order_num=order_num)
            if order:
                order = order[0]
                order.order_status = order_status
                order.trade_no = trade_no
                order.pay_time = datetime.now()
                order.save()

                member_duration = MemberDuration.objects.get(price=order.order_price)
                member_time = datetime.timedelta(days=member_duration.duration)
                ticket_num = member_duration.ticket_num
                member = Member.filter_member(order.order_user)
                if member:
                    member.ticket_num += ticket_num
                    member.deadline += member_time
                    member.save()
                else:
                    deadline = datetime.datetime.now() + member_time
                    Member.objects.create(member_user=order.order_user, ticket_num=ticket_num, deadline=deadline)
            return redirect(reverse('index'))

    @staticmethod
    def post(request):
        """异步回调"""
        data = {}
        for key, value in request.POST.items():
            data[key] = value
        signature = data.pop("sign", None)
        if alipay.verify(data, signature):
            order_num = data.get('out_trade_no', None)
            trade_no = data.get('trade_no', None)
            order_status = data.get('trade_status', None)

            order = Order.objects.filter(order_num=order_num)
            if order:
                order = order[0]
                order.order_status = order_status
                order.trade_no = trade_no
                order.pay_time = datetime.now()
                order.save()

                if order_status in ['TRADE_SUCCESS', 'TRADE_FINISHED']:
                    member_duration = MemberDuration.objects.get(price=order.order_price)
                    member_time = datetime.timedelta(days=member_duration.duration)
                    ticket_num = member_duration.ticket_num
                    member = Member.filter_member(order.order_user)
                    if member:
                        member.ticket_num += ticket_num
                        member.deadline += member_time
                        member.save()
                    else:
                        deadline = datetime.datetime.now() + member_time
                        Member.objects.create(member_user=order.order_user, ticket_num=ticket_num, deadline=deadline)
                return HttpResponse("success")
