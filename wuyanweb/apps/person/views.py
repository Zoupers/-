from django.shortcuts import render, HttpResponse
from django.views import View
from apps.movie.models import Relation, MPR
from .models import Person
from apps.ranking.models import RMR
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.


class PersonView(View):

    def get(self, request):
        person_id = request.GET.get("id", None)
        person = Person.objects.filter(id=person_id)[0]
        image = json.loads(person.image)
        pre_rel_person = MPR.objects.filter(person_id=person_id)
        final_list = []
        movie_list = []
        person_dict = dict()
        for one_person in pre_rel_person:
            if one_person.movie not in movie_list:
                movie_list.append(one_person.movie)
                for same_movie_person in MPR.objects.filter(movie_id=one_person.movie_id):
                    if same_movie_person.person_id == person_id:
                        continue
                    person_dict[same_movie_person] = person_dict.get(same_movie_person, 0)+1
        for m, i in person_dict.items():
            if i > 2:
                final_list.append(m)
        if len(final_list) < 5:
            final_list.extend(list(person_dict.keys())[0:(5-len(final_list))])
        return render(request, "person.html", {
            "actor": person,
            "image": image[:5],
            "image_count": len(image),
            "Like": Relation.objects.filter(person_id=person_id, user_id=request.user.id, type=2),
            'cooperator': final_list[0:5],
            'playMovie': movie_list[0:5]
        })

@csrf_exempt
def take_relation(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        id = request.GET.get('id', None)
        user_id = request.GET.get('user_id')
        list_ = Relation.objects.filter(user_id=user_id, person_id=id, type=2)
        if list_:
            list_[0].delete()
        else:
            person = Relation(user_id=user_id, person_id=id, type=2)
            person.save()
        return HttpResponse('')


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
