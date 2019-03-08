from django.shortcuts import render, HttpResponse, Http404, redirect
from django.views import View

from .models import Movie, MPR, Comment
import json
# Create your views here.


class MovieView(View):

    def get(self, request):
        movie_id = request.GET.get('id')
        if not movie_id:
            return redirect('apps.movie:ranking')
        movie = Movie.objects.filter(id=movie_id)[0]
        cast = MPR.objects.filter(movie_id=movie_id)
        images = json.loads(movie.image)
        image = json.loads(movie.image)[:5]
        comments = Comment.objects.filter(movie_id=movie_id).order_by('-comment_time')
        return render(request, 'movie_base.html', {'movie': movie,
                                                   'cast': cast[:9],
                                                   'image': image[:4],
                                                   'person_count': len(cast),
                                                   'image_count': len(images),
                                                   'comments': comments[:10],
                                                   'comment_num': len(comments)})


class CastView(View):

    def get(self, request):
        movie_id = request.GET.get('id')
        movie_cast = MPR.objects.filter(movie_id=movie_id)
        if not movie_cast:
            raise Http404(request)
        num_actor = len(movie_cast.filter(type='3'))
        l = num_actor % 6
        if l == 0:
            n = int(num_actor/6)
        else:
            n = int(num_actor/6) + 1
        height = n * 210
        return render(request, 'movie_cast.html', {'mpr': movie_cast, 'height': height, 'movie': movie_cast[0].movie})


class PhotoView(View):

    def get(self, request):
        movie_id = request.GET.get('id')
        movie = Movie.objects.filter(id=movie_id)
        if not movie:
            raise Http404(request)
        movie = movie[0]
        photo = json.loads(movie.image)
        return render(request, 'movie_photo.html', {'movie': movie, 'image': photo, 'image_count': len(photo)})


class CommentView(View):

    def post(self, request):
        comment = Comment()
        comment.movie_id = request.POST.get('movie_id')
        comment.user_id = request.POST.get('user_id')
        comment.comment = request.POST.get('comment')
        comment.rank = int(request.POST.get('rank'))
        comment.user_name = request.POST.get('user_name')
        comment.save()
        return HttpResponse('')

    def get(self, request):
        comment_ = Comment.objects.filter(movie_id=request.GET.get('id')).order_by('-comment_time')
        # comments = request.GET.get()
        num = int(request.GET.get('n'))
        comments = comment_[num:num+5]
        final = []
        for i in comments:
            comment = dict()
            comment['user_name'] = i.user_name
            if i.image:
                comment['poster'] = '/static/'+(i.image.replace('\\', '/'))
            else:
                i.image = ''
            comment['comment'] = i.comment
            comment['comment_time'] = str(i.comment_time)
            final.append(comment)
        return HttpResponse(json.dumps(final, ensure_ascii=False), content_type='application/json')


