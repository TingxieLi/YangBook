import xadmin
from .models import Order, MemberDuration


class OrderXadmin(object):
    list_display = ['order_user', 'order_price', 'order_status', 'trade_no', 'pay_time', 'order_num']
    search_fields = ['order_user']
    model_icon = 'fa fa-sticky-note'


class MemberDurationXadmin(object):
    list_display = ['price', 'duration', 'ticket_num', 'create_time', 'update_time']
    model_icon = 'fa fa-sticky-note'


xadmin.site.register(Order, OrderXadmin)
xadmin.site.register(MemberDuration, MemberDurationXadmin)
