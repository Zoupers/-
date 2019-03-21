from django.shortcuts import render, redirect, HttpResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.views import View
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.views import auth_login, auth_logout
from django.contrib.auth.hashers import make_password, check_password
from .form import UserForm
from . import email as email_sent
from apps.movie.models import Comment
from .models import Registing_User, Reset_User
import json

# Create your views here.


class UserView(View):

    def get(self, request):
        if request.user.is_authenticated:
            user_name = request.user.username
            user = User.objects.get(username=user_name)
            comments = Comment.objects.filter(user_id=user.id).order_by('-comment_time')
            if len(comments)>8:
                havemore = True
            else:
                havemore = False
            return render(request, 'user.html', {'user': user, 'comments': comments[:8], 'havemore': havemore})
        else:
            return redirect('apps.user:login')


class LikeView(View):
    def get(self, request):
        pass


class CommentsView(View):
    def get(self, request):
        count = request.GET.get('commentsCount', None)
        if not count:
            return redirect('apps.user:home')
        count = int(count)
        user = request.user
        comment = Comment.objects.filter(user_id=user.id).order_by('-comment_time')
        comments = []
        for i in comment:
            c = dict()
            c['commentTime'] = i.comment_time.__str__()
            c['comment'] = i.comment
            c['movie'] = i.movie.name
            comments.append(c)
        return HttpResponse(json.dumps(comments, ensure_ascii=False), content_type='application/json')


def captcha():
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha


def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


# 登录
class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # request.session.flush()
            return redirect('apps.user:home')

        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        user_form = UserForm()
        return render(request, 'login.html', {'user_form': user_form, 'image_url': image_url, 'hashkey': hashkey})

    def post(self, request, *args, **kwargs):
        form = dict()
        form['userName'] = request.POST.get('userName')
        form['userPassword'] = request.POST.get('userPassword')
        form['captcha'] = request.POST.get('captcha')
        user_form = UserForm(request.POST)
        # print(user_form.is_valid())
        if user_form.is_valid():
            username = user_form.cleaned_data['userName']
            password = user_form.cleaned_data['userPassword']
            try:
                user = User.objects.filter(Q(username=username)|Q(email=username))
                if check_password(password, user[0].password):
                    auth_login(request, user[0])
                    # request.session['is_login'] = True
                    # request.session['user_id'] = user[0].id
                    # request.session['user_name'] = user[0].username
                    # request.user.is_authenticated = True
                    message = '登录成功'
                    return redirect('apps.user:home')
                else:
                    message = '密码不正确！'
            except Exception as e:
                # print(e)
                message = '用户不存在！'
            return render(request, 'login.html', {'js': message})
        else:
            if user_form.errors['captcha'][0]:
                return render(request, 'login.html', {'js': user_form.errors['captcha'][0]})
            return render(request, 'login.html', {'js': "输入错误！"})


# 注册
def register(request):
    if request.user.is_authenticated:
        return redirect('/user/home/')

    if request.method == 'POST':
        username = request.POST.get('userName', '').strip()
        password1 = request.POST.get('userPassword1', '').strip()
        password2 = request.POST.get('userPassword2', '').strip()
        email = request.POST.get('email',None)
        if username and password1 and password2 and email:
            if password1 != password2:
                message = '两次密码输入不一致，请重新输入'
                return render(request,'register.html',locals())
            else:
                same_name = User.objects.filter(username=username)
                if same_name:
                    message = '用户名已存在，请重新输入'
                    return render(request,'register.html', {'js': message})

                same_email = User.objects.filter(email=email)
                if same_email:
                    message = '此邮箱已注册，请重新输入'
                    return render(request,'register.html', {'js': message})
                else:
                    try:
                        res,msg = email_sent.send_A_email(email,username)
                    except:
                        return render(request,'register.html', {'js': "邮箱错误"})
                    if res == 1:
                        Email = '邮件发送成功，请在三天内激活您的账号'
                    else:
                        Email = '邮件发送失败'
                new_user = Registing_User.objects.create()
                new_user.name = username
                new_user.Email_code = msg
                new_user.password = make_password(password1)
                new_user.email = email
                new_user.save()
                return render(request,'register.html', {'js': Email})
        else:
            message = '请将信息填写完整'
            return render(request,'register.html', {'js': message})

    return render(request,'register.html')


# 注册后激活
def active(request):
    if request.method == 'GET':
        request.encoding = 'gb2312'
        token = request.GET.get('token')
        register_name = request.GET.get('name')
        has_active = User.objects.filter(username=register_name)
        if has_active:
            return HttpResponse('已经激活')
        registing = Registing_User.objects.filter(name=register_name)
        if token == registing[0].Email_code:
            new_user = User.objects.create()
            new_user.username = registing[0].name
            new_user.password = registing[0].password
            new_user.email = registing[0].email
            new_user.save()
            registing.delete()
            return render(request, 'email.html', {'message': '激活账号成功'})
        else:
            return render(request, 'email.html', {'message': '激活账号失败'})

    return redirect('apps.user:login')


# 找回密码
def reset(request):
    if request.user.is_authenticated:
        return redirect('/ranking/')

    if request.method == 'POST':
        # username = request.POST.get('userName',None)
        email = request.POST.get('email', None)
        password1 = request.POST.get('userPassword1', None)
        password2 = request.POST.get('userPassword2', None)
        if email and password1 and password2:
            # username = username.strip()
            user = User.objects.filter(email=email)
            if user:
                username = user[0].username
                if password1 != password2:
                    message = '两次密码输入不一致，请重新输入'
                    return render(request, 'reset.html', {'js': message})
                else:
                    # 注意邮件地址的修改
                    res, msg = email_sent.send_B_email(user[0].email, username)
                    if res == 1:
                        Email = '邮件发送成功'
                        new_user = Reset_User.objects.create()
                        new_user.name = username
                        new_user.Email_code = msg
                        new_user.password = password1
                        new_user.save()
                    else:
                        Email = '邮件发送失败'
        else:
            return render(request, 'reset.html', {'js': '有错误'})

    return render(request, 'reset.html', locals())


# 改密验证
def reactive(request):
    if request.method == 'GET':

        token = request.GET.get('token')
        resetting_name = request.GET.get('name')
        if not token and resetting_name:
            return render(request, 'email.html', {'message': '您的链接不正确'})
        resetting = Reset_User.objects.get(name=resetting_name)
        if token == resetting.Email_code:
            new_user = User.objects.get(username=resetting_name)
            new_user.username = resetting.name
            new_user.set_password(resetting.password)
            # new_user.password = make_password(resetting.password)
            new_user.save()
            resetting.delete()
            return render(request, 'email.html', {'message': '验证成功'})
        else:
            return render(request, 'email.html', {'message': '验证失败'})

    return render(request, 'email.html', locals())


# 注销
def logout(request):
    # request.session.flush()
    auth_logout(request)
    return redirect('/ranking/')

