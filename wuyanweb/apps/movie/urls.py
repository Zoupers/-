from django.urls import path
from .views import MovieView

urlpatterns = [
    path('test/', MovieView.as_view(), name='ranking')
]
