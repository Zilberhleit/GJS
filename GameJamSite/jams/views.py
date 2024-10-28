import datetime

from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView
from jams.models import GameJams, UploadFile
from users.forms import UploadGameForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UploadGameForm()
        return context


def game_jam_upload(request, uuid):
    if request.method == "POST":
        if "game" in request.FILES:
            game_file = request.FILES["game"]
            game_extension = '.zip'
            if game_extension in game_file.name:
                instance = UploadFile.objects.create(file=game_file, jam_uuid=get_object_or_404(GameJams, uuid=uuid))
                instance.save()
                return GameJamDetail.as_view() #render(request, 'jams_list')
        return HttpResponseNotFound(render(request, "pages/errors/404.html"))


def handler404(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(render(request, "pages/errors/404.html"))
