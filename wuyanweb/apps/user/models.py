from django.db import models

# Create your models here.


#待激活中账户
class Registing_User(models.Model):

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    Email_code = models.CharField(max_length=128)

#改密待验证中账户
class Resetting_User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    Email_code = models.CharField(max_length=128)

#已注册账户
class User(models.Model):

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)


    class Mate:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


