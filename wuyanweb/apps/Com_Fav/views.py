from django.shortcuts import render
from .models import MovieComments, UserFavorite
from django.http import HttpResponse
from django.views.generic.base import View
from movie.models import Movie
# Create your views here.


class CommentsView(View):
    # 评论页面
    # 这里需要一个包含Movie基础信息的

    def get(self, request, movie_id):
        movie = Movie.objects.get(id=int(movie_id))
        all_comments = MovieComments.objects.all()
        return render(request, "movie_comment.html", {
            "movie": movie,
            "all_comments": all_comments
        })


class AddCommentsView(View):
    # 添加评论后的页面

    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        movie_id = request.POST.get("movie_id", 0)
        comments = request.POST.get("comments", "")
        if movie_id > 0 and comments:
            movie_comments = MovieComments()
            movie = Movie.objects.get(id=int(movie_id))
            movie_comments.movie = movie
            movie_comments.comments = comments
            movie_comments.user = request.user
            movie_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class AddFavView(View):
    # 收藏及取消收藏影片
    @staticmethod
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', '')

        if request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果已经收藏，表示用户取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')
