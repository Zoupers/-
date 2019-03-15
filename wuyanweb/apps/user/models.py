from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from apps.movie.models import Movie
from apps.person.models import Person


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


class Relation(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    movie_id = models.CharField(max_length=50, default=None, blank=True)
    person_id = models.CharField(max_length=50, default=None, blank=True)
    type = models.CharField(choices=((1, '电影'), (2, '人物')), max_length=3)

    class Meta(object):
        pass
    



