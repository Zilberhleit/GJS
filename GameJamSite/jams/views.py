from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from jams.models import GameJams, UploadFile
from users.models import User


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


def game_jam_upload(request, uuid):
    if request.method == "POST":
        if "game" in request.FILES:
            game_file = request.FILES["game"]
            game_extension = '.zip'
            if game_extension in game_file.name:
                instance = UploadFile.objects.create(file=game_file, jam_uuid=get_object_or_404(GameJams, uuid=uuid),
                                                     user=get_object_or_404(User, username=request.user))
                instance.save()
                return render(request, 'pages/jams_pages/jams.html')
        return HttpResponseNotFound(render(request, "pages/errors/404.html"))


def handler404(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(render(request, "pages/errors/404.html"))
