# from django.contrib import admin
import xadmin

from .models import Movie, MPR
# Register your models here.


class MovieAdmin(object):
    list_display = ['id', 'name', 'rank', 'star_num', 'year']
    search_fields = ['name', 'id']
    list_editable = []
    list_filter = ['rank', 'star_num']


class MPRAdmin(object):
    list_display = ['_type', 'movie', 'person']
    search_fields = ['person__id', 'person__name', '_type']
    list_editable = []
    list_filter = ['movie__name', 'movie__id', '_type']


xadmin.site.register(Movie, MovieAdmin)
xadmin.site.register(MPR, MPRAdmin)
