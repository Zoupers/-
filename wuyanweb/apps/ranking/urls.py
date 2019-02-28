from django.urls import path
from .views import RankingView, BoxOfficeView, NowPlayingView, ChartView

urlpatterns = [
    path('', RankingView.as_view(), name='ranking'),
    path('top250/', RankingView.as_view(), name='top250'),
    path('chart/', ChartView.as_view(), name='chart'),
    path('boxoffice/', BoxOfficeView.as_view(), name='box_office'),
    path('nowplaying/', NowPlayingView.as_view(), name='now_playing')
]