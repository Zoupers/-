from django.urls import path
from .views import PersonView, PhotoView

urlpatterns = [
    path('', PersonView.as_view(), name='person'),
    path('photo/', PhotoView.as_view(), name='person_photo')
]