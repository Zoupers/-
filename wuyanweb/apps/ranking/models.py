from django.db import models
from apps.movie.models import Movie
# Create your models here.


class RMR(models.Model):
    _type = models.CharField(max_length=10, verbose_name='排行榜种类')
    rank = models.IntegerField(verbose_name='排名')
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING, verbose_name='电影')

    class Meta(object):
        verbose_name = '电影排行榜'
        verbose_name_plural = verbose_name
