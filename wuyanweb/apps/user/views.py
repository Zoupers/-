from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.core.mail import send_mail,send_mass_mail
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.views import View
from user import email as email_sent
from user.models import User,Registing_User,Resetting_User
from django.contrib.auth.hashers import make_password,check_password
from user.form import UserForm
import json
# Create your views here.





def captcha():
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha

def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')

#登录
def login(request):
    if request.session.get('is_login',None):
        request.session.flush()
        return redirect('/index')

    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    user_form = UserForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['userName']
            password = user_form.cleaned_data['userPassword']
            try:
                user = User.objects.filter(name=username)
                if check_password(password, user[0].password) == True:
                    request.session['is_login'] = True
                    request.session['user_id'] = user[0].id
                    request.session['user_name'] = user[0].name
                    message = '登录成功'
                    return render(request, 'login.html', locals())
                else:
                    message = '密码不正确！'
            except:
                message = '用户不存在！'
        return render(request,'login.html',locals())

    return render(request,'login.html',locals())



#注册
def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')

    if request.method == 'POST':
        username = request.POST.get('userName',None)
        password1 = request.POST.get('userPassword1',None)
        password2 = request.POST.get('userPassword2',None)
        email = request.POST.get('email',None)
        if username and password1 and password2 and email:
            if password1 != password2:
                message = '两次密码输入不一致，请重新输入'
                return render(request,'register.html',locals())
            else:
                same_name = User.objects.filter(name=username)
                if same_name:
                    message = '用户名已存在，请重新输入'
                    return render(request,'register.html',locals())

                same_email = User.objects.filter(email=email)
                if same_email:
                    message = '此邮箱已注册，请重新输入'
                    return render(request,'register.html',locals())
                else:
                    res,msg = email_sent.send_A_email(email,username)
                    if res == 1:
                        Email = '邮件发送成功'
                    else:
                        Email = '邮件发送失败'
                new_user = Registing_User.objects.create()
                new_user.name = username
                new_user.Email_code = msg
                new_user.password = make_password(password1)
                new_user.email = email
                new_user.save()
                return render(request,'register.html',locals())
        else:
            message = '请将信息填写完整'

    return render(request,'register.html',locals())

#注册后激活
def active(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        register_name = request.GET.get('name')
        registing = Registing_User.objects.filter(name=register_name)
        if token == registing[0].Email_code:
            new_user = User.objects.create()
            new_user.name = registing[0].name
            new_user.password = registing[0].password
            new_user.email = registing[0].email
            new_user.save()
            registing.delete()
            return HttpResponse('激活成功')
        else:
            return HttpResponse('激活失败')

    return render(request,'email.html',locals())





#找回密码
def reset(request):
    if request.session.get('is_login',None):
        return redirect('/index/')

    if request.method == 'POST':
        username = request.POST.get('userName',None)
        password1 = request.POST.get('userPassword1', None)
        password2 = request.POST.get('userPassword2', None)
        if username:
            username = username.strip()
            user = User.objects.filter(name=username)
            if password1 != password2:
                message = '两次密码输入不一致，请重新输入'
                return render(request, 'reset/reset.html', locals())
            else:
                res, msg = email_sent.send_B_email(user[0].email, username)
                if res == 1:
                    Email = '邮件发送成功'
                    new_user = Resetting_User.objects.create()
                    new_user.name = username
                    new_user.Email_code = msg
                    new_user.password = make_password(password1)
                    new_user.save()
                else:
                    Email = '邮件发送失败'

    return render(request,'reset.html',locals())


#改密验证
def reactive(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        resetting_name = request.GET.get('name')
        resetting = Resetting_User.objects.filter(name=resetting_name)
        if token == resetting[0].Email_code:
            new_user = User.objects.filter(name=resetting_name)
            new_user[0].name = resetting[0].name
            new_user[0].password = resetting[0].password
            new_user[0].save()
            resetting.delete()
            return HttpResponse('验证成功')
        else:
            return HttpResponse('验证失败')

    return render(request,'email.html',locals())

#注销
def logout(request):
    if request.session.get('is_login',None):
        request.session.flush()
        return redirect('/user')

