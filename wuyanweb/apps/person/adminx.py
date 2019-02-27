# from django.contrib import admin

import xadmin
# Register your models here.
from .models import Person


class PersonAdmin(object):
    list_display = ['id', 'name', 'sex', 'birthday', 'imdb', 'introduce']
    search_fields = ['id', 'name', 'sex', 'imdb', 'birthday', 'birthplace']
    list_editable = []
    list_filter = ['id', 'name', 'sex', 'imdb', 'birthday', 'birthplace']


xadmin.site.register(Person, PersonAdmin)