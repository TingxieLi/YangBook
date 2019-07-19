from django import forms
from django.db.models import Q
from user.models import UserInfo
from .models import MemberDuration


class OrderForm(forms.Form):
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '邮箱格式错误'
        }
    )

    price = forms.IntegerField(
        required=True,
        error_messages={
            'required': '价格不能为空',
            'invalid': '价格必须是数字类型'
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not UserInfo.objects.filter(Q(username=email) | Q(email=email)):
            raise forms.ValidationError('该用户不存在')
        return email

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if not MemberDuration.objects.filter(price=price):
            raise forms.ValidationError('价格信息错误')
        return price
