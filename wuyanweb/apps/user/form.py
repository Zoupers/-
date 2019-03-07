from django import forms
# from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField


# class UserForm(User):
#     username = forms.CharField(label='用户名', max_length=20)
#     password = forms.CharField(label='密码', max_length=18)
#     email = forms.EmailField(label='邮箱', required=True)
#     is_active = forms.IntegerField(label='激活')
#     captcha = CaptchaField()

class UserForm(forms.Form):
    userName = forms.CharField(label='用户名',max_length=128)
    userPassword = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput)
    captcha = CaptchaField()
