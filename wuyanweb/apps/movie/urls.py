from django.urls import path
from .views import MovieView, CastView

urlpatterns = [
    path('', MovieView.as_view(), name='ranking'),
    path('cast/', CastView.as_view(), name='movie_cast')
]
