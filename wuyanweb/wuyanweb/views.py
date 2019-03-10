from django.views import View
from django.shortcuts import redirect


class IndexView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('apps.ranking:ranking')
        else:
            return redirect('apps.user:login')

