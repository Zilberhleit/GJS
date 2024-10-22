from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render
import uuid
from django.views.generic import ListView, DetailView
from jams.models import GameJams


class GameJamsLists(ListView):
    template_name = 'pages/jams_pages/jams.html'
    context_object_name = "jams_list"
    queryset = GameJams.objects.all()


class GameJamDetail(DetailView):
    model = GameJams
    template_name = 'pages/jams_pages/gamejam_detail.html'
    context_object_name = "gamejam_detail"
    def get_object(self, queryset=None):
        return GameJams.objects.get(uuid=self.kwargs.get("uuid"))


def handler404(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(render(request, "pages/errors/404.html"))
