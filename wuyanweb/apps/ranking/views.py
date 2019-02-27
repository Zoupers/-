from django.shortcuts import render
from django.views import View
from .models import RMR
# Create your views here.


def page(film, num, start, _type=None):
    """

    :param film: 总的电影的集合
    :param num: 每页的个数
    :param start: 从多少开始
    :return:
    """
    l = len(film)
    if l % num == 0:
        page_num = int(l/num)
    else:
        page_num = int(l/num+1)
    now = int(start / num + 1)
    if _type:
        final = [(int(i+1), '?start=%d&type=' % (num * int(i))+_type) for i in range(page_num)]
    else:
        final = [(int(i+1), '?start=%d' % (num * int(i))) for i in range(page_num)]
    if now > 1:
        prev = now-1
        prev_url = '?start=%d' % ((prev-1)*num) if not _type else ('?start=%d&type=' % ((prev-1)*num)+_type)
    else:
        prev = None
        prev_url = None
    if now != page_num:
        _next = now
        next_url = '?start=%d' % (_next*num) if not _type else ('?start=%d&type=' % (_next*num)+_type)
    else:
        _next = None
        next_url = None
    return {'now': now, 'final': final, 'total': l, 'prev': prev, 'prev_url': prev_url, 'next': _next, 'next_url': next_url}


class RankingView(View):

    def get(self, request):
        movie = RMR.objects.filter(_type='top250').order_by('rank')
        num = 10
        start = int(request.GET.get('start'))
        if request.GET.get('type'):
            _type = request.GET.get('type')
            movie = RMR.objects.filter(_type=_type).order_by('rank')
            pages = page(movie, num, start, _type=_type)
        else:
            pages = page(movie, num, start)
        if not start:
            start = 0
        if start or start == 0:
            if start % num == 0 or start == 0:
                movies = movie[start:start+10]
                return render(request, 'ranking.html', {'movies': movies, 'pages': pages})
            else:
                return
        movies = movie[:10]
        return render(request, 'ranking.html', {'movies': movies})
