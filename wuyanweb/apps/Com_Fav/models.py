from django.db import models
from datetime import datetime
from apps.user.models import User
from apps.movie.models import Movie


class MovieComments(models.Model):
        # 电影评论
        # 这里需要接口model.py中的有关用户User和有关电影Movie数据
        user = models.ForeignKey(User, verbose_name="用户", on_delete=models.DO_NOTHING)
        movie = models.ForeignKey(Movie, verbose_name="电影", on_delete=models.DO_NOTHING)
        comments = models.CharField(max_length=200, verbose_name="评论")
        add_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")

        class Meta:
                verbose_name = u"课程评论"
                verbose_name_plural = verbose_name


class UserFavorite(models.Model):
        # 影片及演员收藏
        # 需要User
        user = models.ForeignKey(User, verbose_name="用户", on_delete=models.DO_NOTHING)
        fav_id = models.IntegerField(default=0, verbose_name=u"收藏数据id")
        fav_type = models.IntegerField(choices=((1, "电影"), (2, "演员")), default=1, verbose_name="收藏类型")
        add_time = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

        class Meta:
                verbose_name = u"用户收藏"
                verbose_name_plural = verbose_name
