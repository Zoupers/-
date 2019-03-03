from django.shortcuts import render, HttpResponse
from django.views import View
# Create your views here.
from apps.movie.models import Movie
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
        result.extend(Movie.objects.filter(name__icontains=msg))
    return result


class ResearchView(View):

    def get(self, request):
        pass

    def post(self, request):
        msg = request.POST.get('msg')
        if msg.isdigit():
            result = search(msg, mode=1)
        elif msg:
            result = search(msg, mode=2)
        else:
            return render(request, 'search.html', {})
        if result:
            result_left = [result[i] for i in range(len(result)) if i % 2 == 0]
            result_right = [result[i] for i in range(len(result)) if i % 2 != 0]
            return render(request, 'search.html', {'result_left': result_left, 'result_right': result_right})
        else:
            return render(request, 'search.html', {'result': None})


