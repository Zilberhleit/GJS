from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
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

#Нужно найти способ передать в класс uuid, чтобы его записало в модель UploadFile
class GameJamUpload(CreateView):
    fields = ['file', 'jam_uuid']
    form_class = UploadGameForm
    model = UploadFile

def game_jam_upload(request, uuid):
    if request.method == "POST":
        instance = GameJamUpload.objects.create(file=file, jam_uuid=uuid)

        instance.save()


def handler404(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(render(request, "pages/errors/404.html"))
