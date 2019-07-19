from django.db import models
from db.base_model import BaseModel
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class UserInfo(AbstractUser, BaseModel):
    avatar = models.ImageField(upload_to='user/', verbose_name='头像', null=True, blank=True)
    nickname = models.CharField(max_length=20, verbose_name='昵称', null=True, blank=True)
    address = models.CharField(max_length=20, verbose_name='地址', null=True, blank=True)
    gender = models.CharField(choices=(('girl', '女'), ('boy', '男')), max_length=10, verbose_name='用户性别', default='girl')
    phone = models.CharField(max_length=11, verbose_name='用户手机', null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class Member(BaseModel):
    deadline = models.DateTimeField(verbose_name='到期时间')
    ticket_num = models.IntegerField(default=0, verbose_name='推荐票数')
    member_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='会员用户')

    @classmethod
    def filter_member(cls, user):
        member = cls.objects.filter(deadline__gt=datetime.now(), member_user=user)
        if member:
            member = member[0]
        else:
            member = None
        return member

    def __str__(self):
        return self.member_user.username

    class Meta:
        verbose_name = '会员信息'
        verbose_name_plural = verbose_name
