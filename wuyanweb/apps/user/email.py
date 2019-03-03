from django.core.mail import send_mail
from wuyanweb import settings
import random


def random_str():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(6):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


# 注册账号验证
def send_A_email(req,name):
    title = '云顶电影注册'
    reciever = []
    reciever.append(req)
    random = random_str()
    msg = '打开此链接激活账户：http://127.0.0.1:8000/active/?token='+random+'&name='+name
    res = send_mail(title, msg,settings.EMAIL_HOST_USER, reciever)
    return res,random


# 改密验证
def send_B_email(req,name):
    title = '云顶电影密码找回'
    reciever = []
    reciever.append(req)
    random = random_str()
    msg = '打开此链接激活账户：http://127.0.0.1:8000/reactive/?token='+random+'&name='+name
    res = send_mail(title, msg,settings.EMAIL_HOST_USER, reciever)
    return res,random
