from django.shortcuts import render, HttpResponse
from django.views import View
from django.core import serializers
from .models import Movie
import json
# Create your views here.
from .models import MPR


class MovieView(View):

    def get(self, request):
        return


class CastView(View):

    def get(self, request):
        movie_id = request.GET.get('id')
        movie_cast = MPR.objects.filter(movie_id=movie_id)
        return render(request, 'cast.html', {'mpr': movie_cast})
