from django.shortcuts import render, HttpResponse, Http404
from django.views import View
# Create your views here.
from apps.movie.models import Movie, MPR
from apps.person.models import Person


def search(msg, mode):
    """

    :param msg:
    :param mode: if 1 search person or movie by id
                 if 2 search name
    :return:
    """
    result = []
    if mode == 1:
        result.extend(Movie.objects.filter(id=msg))
        result.extend(Person.objects.filter(id=msg))
    elif mode == 2:
        result.extend(Movie.objects.filter(name__icontains=msg))
        result.extend(Person.objects.filter(name__icontains=msg))
    return result


class ResearchView(View):

    def get(self, request):
        raise Http404()

    def post(self, request):
        msg = request.POST.get('msg')
        if msg.isdigit():
            result = search(msg, mode=1)
        elif msg:
            result = search(msg, mode=2)
        else:
            return render(request, 'search.html', {})
        if result:
            result_left = list(set([result[i] for i in range(len(result)) if i % 2 == 0]))
            result_right = list(set([result[i] for i in range(len(result)) if i % 2 != 0]))
            person = []
            for m in result_left+result_right:
                if hasattr(m, 'rank'):
                    person.extend(MPR.objects.filter(movie_id=m.id))
            return render(request, 'search.html', {'result_left': result_left, 'result_right': result_right, 'person': person})
        else:
            return render(request, 'search.html', {'result': None})

