# from django.contrib import admin
import xadmin
from .models import RMR
# Register your models here.


class RMRAdmin(object):
    list_display = ['_type', 'rank', 'movie']
    search_fields = ['_type', 'movie__name', 'rank']
    list_editable = []
    list_filter = ['_type', 'rank']


xadmin.site.register(RMR, RMRAdmin)
