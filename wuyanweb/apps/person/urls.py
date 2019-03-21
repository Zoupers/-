from django.urls import path
from .views import PersonView, PhotoView, take_relation

urlpatterns = [
    path('', PersonView.as_view(), name='person'),
    path('relation/', take_relation, name='relation'),
    path('photo/', PhotoView.as_view(), name='person_photo')
]