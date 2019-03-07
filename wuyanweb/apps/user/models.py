from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# 待激活中账户
class Registing_User(models.Model):
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    Email_code = models.CharField(max_length=128)
    poster = models.CharField(max_length=50, null=True)


# 改密待验证中账户
class Reset_User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    Email_code = models.CharField(max_length=128)


# 已注册账户
# class User(BaseUser):
#     poster = models.CharField(max_length=50, verbose_name='用户头像', null=True, blank=True)
#     motto = models.CharField(max_length=200, null=True, verbose_name='座右铭', blank=True)
#     introduce = models.TextField(verbose_name='个人简介', null=True, blank=True)




