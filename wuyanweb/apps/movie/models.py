from django.db import models
from apps.person.models import Person
# Create your models here.


class Movie(models.Model):
    """
    电影的数据表
    """
    name = models.CharField(max_length=30, null=False, verbose_name='影名')
    long = models.CharField(max_length=60, null=True, verbose_name='片长')
    rank = models.FloatField(verbose_name='评分')
    star_num = models.CharField(max_length=15, null=True, verbose_name='评价人数')
    year = models.CharField(max_length=100, null=True, verbose_name='上映日期')
    _class = models.CharField(max_length=50, null=True, verbose_name='类型')
    countries = models.CharField(max_length=50, null=True, verbose_name='制片国家/地区')
    id = models.IntegerField(verbose_name='ID', unique=True, primary_key=True)
    review = models.TextField(verbose_name='简评', null=True)
    # 注意，这个details中的信息是电影详情页中的信息
    details = models.TextField(verbose_name='详细信息', null=True)
    poster = models.CharField(verbose_name='电影海报', max_length=60, default=None, null=True)
    image = models.TextField(verbose_name='电影剧照', default=None, null=True)

    class Meta(object):
        verbose_name = '电影'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MPR(models.Model):
    """
    电影与演员的关系
    """
    type = models.CharField(max_length=10, verbose_name='职位', choices=(('1', '导演'), ('2', '编剧'), ('3', '演员')))
    movie = models.ForeignKey(Movie, null=True, on_delete=models.SET_NULL, verbose_name='电影')
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, verbose_name='人物')
    part = models.TextField(verbose_name='角色', default=None, null=True, blank=True)

    class Meta(object):
        verbose_name = '电影演员关系'
        verbose_name_plural = verbose_name

