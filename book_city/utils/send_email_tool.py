from django.core.mail import send_mail
from django_redis import get_redis_connection
from random import randrange
from django.conf import settings


def get_random_code(code_length):
    code_source = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(code_length):
        code += code_source[randrange(0, len(code_source)-1)]
    return code


def send_email_code(email, send_type):
    conn = get_redis_connection('default')
    email_key = '{}_{}'.format(email, send_type)
    if conn.get(email_key):
        msg = '请60s后重试'
    else:
        code = get_random_code(8)
        conn.set(email_key, code)
        conn.expire(email_key, 60)
        sender = settings.EMAIL_FROM
        receiver = [email]
        subject = ''
        if send_type == '1':
            subject = '欢迎注册阳哥书城'
        if send_type == '2':
            subject = '阳哥书城-重置密码'
        message = code
        send_mail(subject, message, sender, receiver)
        msg = '验证码已发送至你的邮箱'
    return msg

