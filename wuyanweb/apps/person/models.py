from django.db import models

# Create your models here.


class Person(models.Model):
    """
    id, name, sex, constellation, birthday, birthplace, profession, imdb, introduce
    """
    id = models.IntegerField(null=False, blank=False, primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=False, verbose_name='姓名')
    sex = models.CharField(max_length=6, null=True, blank=True, verbose_name='性别')
    constellation = models.CharField(max_length=10, null=True, blank=True, verbose_name='星座')
    birthday = models.CharField(max_length=30, null=True, blank=True, verbose_name='生辰')
    birthplace = models.CharField(max_length=100, null=True, blank=True, verbose_name='出生地')
    profession = models.CharField(max_length=60, null=True, blank=True, verbose_name='职业')
    imdb = models.CharField(max_length=15, null=True, blank=True, verbose_name='IMDB编号')
    introduce = models.TextField(verbose_name='简介', null=True, blank=True)
    poster = models.CharField(verbose_name='人物海报', max_length=60, null=True, blank=True)
    image = models.TextField(verbose_name='人物照片', null=True, blank=True)

    class Meta(object):
        verbose_name = '人物'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


