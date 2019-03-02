from django.urls import path
from .views import MovieView, CastView, PhotoView

urlpatterns = [
    path('', MovieView.as_view(), name='ranking'),
    path('cast/', CastView.as_view(), name='movie_cast'),
    path('photo/', PhotoView.as_view(), name='movie_photo')
]
