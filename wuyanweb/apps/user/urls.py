"""douban_movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserView.as_view(), name='home'),
    path('comment/', views.CommentsView.as_view(), name='comments'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('reset/', views.reset, name='reset'),
    path('refresh_captcha/', views.refresh_captcha, name='refresh_captcha'),
    path('active/', views.active, name='active'),
    path('reactive/', views.reactive, name='reactive'),
    path('logout/', views.logout, name='logout'),
]
