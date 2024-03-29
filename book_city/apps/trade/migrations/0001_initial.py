# Generated by Django 2.0 on 2019-05-14 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberDuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('price', models.IntegerField(verbose_name='费用')),
                ('duration', models.IntegerField(verbose_name='时长')),
                ('ticket_num', models.IntegerField(default=0, verbose_name='推荐票')),
            ],
            options={
                'verbose_name': '会员价格',
                'verbose_name_plural': '会员价格',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('order_status', models.CharField(choices=[('WAIT_BUYER_PAY', '交易创建'), ('TRADE_CLOSED', '超时关闭'), ('TRADE_SUCCESS', '支付成功'), ('TRADE_FINISHED', '交易结束')], default='WAIT_BUYER_PAY', max_length=30, verbose_name='订单状态')),
                ('order_price', models.IntegerField(verbose_name='费用')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='支付时间')),
                ('order_num', models.CharField(blank=True, max_length=100, unique=True, verbose_name='订单号')),
                ('trade_no', models.CharField(blank=True, max_length=128, null=True, verbose_name='支付编号')),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='订单用户')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
            },
        ),
    ]
