from django.shortcuts import render
from django.views import View
from .models import Movie
# Create your views here.


class MovieView(View):

    def get(self, request):
        pass


class CastView(View):

    def get(self, response):
        pass
