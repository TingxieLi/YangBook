from django.db import models
from db.base_model import BaseModel
from user.models import UserInfo
import time


class Order(BaseModel):
    """订单"""
    ORDER_STATUS = (
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_CLOSED", "超时关闭"),
        ("TRADE_SUCCESS", "支付成功"),
        ("TRADE_FINISHED", "交易结束"),
    )
    order_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='订单用户')
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default="WAIT_BUYER_PAY", verbose_name='订单状态')
    order_price = models.IntegerField(verbose_name='费用')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    order_num = models.CharField(max_length=100, blank=True, unique=True, verbose_name='订单号')
    trade_no = models.CharField(max_length=128, null=True, blank=True, verbose_name='支付编号')

    @staticmethod
    def generate_order_num(user_id):
        return "{}{}".format(time.strftime("%Y%m%d%H%M%S"), user_id)

    def __str__(self):
        return self.order_num

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name


class MemberDuration(BaseModel):
    price = models.IntegerField(verbose_name='费用')
    duration = models.IntegerField(verbose_name='时长')
    ticket_num = models.IntegerField(default=0, verbose_name='推荐票')

    def __str__(self):
        return '{}元/{}天'.format(self.price, self.duration)

    class Meta:
        verbose_name = '会员价格'
        verbose_name_plural = verbose_name
