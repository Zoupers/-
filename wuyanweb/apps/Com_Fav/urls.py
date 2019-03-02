from django.urls import path, re_path
from .views import CommentsView, AddCommentsView, AddFavView
app_name = 'comment'
urlpatterns = [
    # 课程评论
    re_path(r'^comment_view/(?P<movie_id>[0-9]+)/$', CommentsView.as_view(), name="movie_comments"),
    # 添加课程评论
    re_path(r'^add_comment/$', AddCommentsView.as_view(), name="add_comment"),
    # 影片收藏
    re_path(r'^add_fav/$', AddFavView.as_view(), name="add_fav")
    # 演员收藏

]
