"""wuyanweb URL Configuration

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
# from django.contrib import admin
from django.urls import path, include
import apps.movie.urls as movie_urls
import apps.person.urls as person_urls
import apps.ranking.urls as ranking_urls
import apps.user.urls as user_urls
from apps.research.views import ResearchView
import captcha.urls
import xadmin

urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('movie/', include((movie_urls, 'apps.movie'), namespace='movie')),
    path('person/', include((person_urls, 'apps.person'), namespace='person')),
    path('ranking/', include((ranking_urls, 'apps.ranking'), namespace='ranking')),
    path('user/', include((user_urls, 'apps.user'), namespace='user')),
    path('search/', ResearchView.as_view(), name='search'),
    path('captcha/', include(captcha.urls))
]
