# from django.contrib import admin
import xadmin
from .models import RMR
# Register your models here.


class RMRAdmin(object):
    list_display = ['type', 'rank', 'movie']
    search_fields = ['type', 'movie__name', 'rank']
    list_editable = []
    list_filter = ['type', 'rank']


xadmin.site.register(RMR, RMRAdmin)
