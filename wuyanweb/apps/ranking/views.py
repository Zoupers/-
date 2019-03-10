from django.shortcuts import render, Http404
from django.views import View
from .models import RMR
from apps.movie.models import MPR
from fake_useragent import FakeUserAgent
import requests
# Create your views here.


classify = list(set([i.type for i in RMR.objects.all() if i.type not in ['top250', '新片榜', '热映榜']]))


def page(film, num, start, _type=None):
    """

    :param film: 总的电影的集合
    :param num: 每页的电影个数
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
        movie = RMR.objects.filter(type='top250').order_by('rank')
        num = 10
        _type = None
        # 将要传进网页的参数
        base = dict()
        # 分类排行榜种类
        base['classify'] = classify
        base['chart_'] = RMR.objects.filter(type='新片榜').order_by('rank')
        base['nowplaying_'] = RMR.objects.filter(type='热映榜').order_by('rank')
        base['boxoffice_'] = box_office()[:10]
        # 加载类别
        all_type = set()
        for movie_ in movie:
            all_type.add(movie_.type)
        # 判断是否有第几页的要求
        if request.GET.get('start'):
            start = int(request.GET.get('start'))
        else:
            start = 0
        # 判断排行榜类别
        if request.GET.get('type'):
            _type = request.GET.get('type')
            movie = RMR.objects.filter(type=_type).order_by('rank')
            pages = page(movie, num, start, _type=_type)
        else:
            pages = page(movie, num, start)
        base['type'] = 'top250' if not _type else _type
        # 有了类别就好这个电影集就好找电影的阵容了
        base['person'] = []
        # 返回对应页数的内容
        if start or start == 0:
            if start % num == 0 or start == 0:
                movies = movie[start:start+10]
                for m in movies:
                    base['person'].extend(MPR.objects.filter(movie_id=m.movie_id))
                base['pages'] = pages
                base['movies'] = movies
                # 根据类别返回内容
                return render(request, 'ranking.html', base)
            else:
                raise Http404


def box_office():
    fake = FakeUserAgent()
    data = ''
    for i in range(5):
        z = requests.get('http://dianying.nuomi.com/movie/boxrefresh',
                         headers={'User-Agent': fake.random, 'referer': 'http://dianying.nuomi.com/movie/boxoffice'})
        try:
            data = z.json() if len(z.text) > 1000 else data
        except:
            continue
    movies = []
    n = 1
    for movie_ in data['real']['data']['detail']:
        movie = dict()
        movie['rank'] = n
        movie['movieName'] = movie_['movieName']
        movie['上映天数'] = movie_['attribute']['1']['attrValue']
        movie['实时票房'] = movie_['attribute']['3']['attrValue']
        movie['累计票房'] = movie_['attribute']['2']['attrValue']
        movie['票房占比'] = movie_['attribute']['4']['attrValue']
        movie['排片占比'] = movie_['attribute']['5']['attrValue']
        movie['上座率'] = movie_['attribute']['6']['attrValue']
        movie['排座占比'] = movie_['attribute']['7']['attrValue']
        movie['场次'] = movie_['attribute']['8']['attrValue']
        movie['人次'] = movie_['attribute']['9']['attrValue']
        movies.append(movie)
        n += 1
    # print(movies)
    return movies


class BoxOfficeView(View):
    """
    国内票房榜
    """
    def get(self, request):
        base = dict()
        base['boxoffice'] = True
        base['classify'] = classify
        base['nowplaying_'] = RMR.objects.filter(type='热映榜').order_by('rank')
        base['chart_'] = RMR.objects.filter(type='新片榜').order_by('rank')
        base['movies'] = box_office()
        return render(request, 'box_office.html', base)


class ChartView(View):
    """
    热议新片榜
    """
    def get(self, request):
        base = dict()
        # 提示哪个排行榜
        base['chart'] = True
        base['classify'] = classify
        base['nowplaying_'] = RMR.objects.filter(type='热映榜').order_by('rank')
        base['boxoffice_'] = box_office()[:10]
        # 获取电影
        movies = RMR.objects.filter(type='新片榜').order_by('rank')
        base['movies'] = movies
        # 加载人物
        base['person'] = []
        for movie in movies:
            base['person'].extend(MPR.objects.filter(movie_id=movie.movie_id))
        return render(request, 'chart.html', base)


class NowPlayingView(View):
    """
    热映高分榜
    """
    def get(self, request):
        base = dict()
        # 提示哪个排行榜
        base['nowplaying'] = True
        base['classify'] = classify
        base['chart_'] = RMR.objects.filter(type='新片榜').order_by('rank')
        base['boxoffice_'] = box_office()[:10]
        # 获取电影
        movies = RMR.objects.filter(type='热映榜')
        base['movies'] = movies
        # 加载人物
        base['person'] = []
        for movie in movies:
            base['person'].extend(MPR.objects.filter(movie_id=movie.movie_id))
        return render(request, 'nowplaying.html', base)
