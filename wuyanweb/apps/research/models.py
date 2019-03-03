from django.db import models

# Create your models here.


class SearchHistory(models.Model):
    content = models.TextField(verbose_name="搜索内容")
    result = models.TextField(verbose_name="搜索结果")
    time = models.DateTimeField(auto_created=True, verbose_name="搜索时间")

    class Meta(object):
        verbose_name = '用户查询历史'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
