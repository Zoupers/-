from django import forms
from captcha.fields import CaptchaField


class UserForm (forms.Form):
    userName = forms.CharField(label='用户名',max_length=128)
    userPassword = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput)
    captcha = CaptchaField()