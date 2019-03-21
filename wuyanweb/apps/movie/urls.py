from django.urls import path
from .views import MovieView, CastView, PhotoView, CommentView, take_relation

urlpatterns = [
    path('', MovieView.as_view(), name='movie'),
    path('relation/', take_relation,name='like'),
    path('cast/', CastView.as_view(), name='movie_cast'),
    path('photo/', PhotoView.as_view(), name='movie_photo'),
    path('comment/', CommentView.as_view(), name='comment')
]
