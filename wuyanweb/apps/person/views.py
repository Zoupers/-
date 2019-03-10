from django.shortcuts import render
from django.views import View
from .models import Person
from apps.ranking.models import RMR
import json
# Create your views here.


class PersonView(View):

    def get(self, request):
        person_id = request.GET.get("id", None)
        person = Person.objects.filter(id=person_id)[0]
        image = json.loads(person.image)
        return render(request, "person.html", {
            "actor": person,
            "image": image[:5],
            "image_count": len(image)
        })


class PhotoView(View):

    def get(self, request):
        person_id = request.GET.get('id', None)
        person = Person.objects.filter(id=person_id)[0]
        image = json.loads(person.image)
        return render(request, "person_photo.html", {
            "person": person,
            "image": image,
            "image_count": len(image)
        })
