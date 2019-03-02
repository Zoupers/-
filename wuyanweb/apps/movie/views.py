from django.shortcuts import render, HttpResponse, Http404
from django.views import View
from django.core import serializers
from .models import Movie
import json
# Create your views here.
from .models import MPR


def test(request):
    return render(request, 'base.html')


class MovieView(View):

    def get(self, request):
        movie_id = request.GET.get('id')
        movie = Movie.objects.filter(id=movie_id)[0]
        return render(request, 'movie_base.html', {'movie': movie})


class CastView(View):

    def get(self, request):
        movie_id = request.GET.get('id')
        movie_cast = MPR.objects.filter(movie_id=movie_id)
        num_actor = len(movie_cast.filter(type='3'))
        l = num_actor % 6
        if l == 0:
            n = int(num_actor/6)
        else:
            n = int(num_actor/6) + 1
        height = n * 185
        return render(request, 'movie_cast.html', {'mpr': movie_cast, 'height': height, 'movie': movie_cast[0].movie})


class PhotoView(View):

    def get(self, request):
        movie_id = request.GET.get('id')
        movie = Movie.objects.filter(id=movie_id)
        if not movie:
            raise Http404(request)
        movie = movie[0]
        photo = json.loads(movie.image)
        return render(request, 'movie_photo.html', {'movie': movie, 'image': photo})
