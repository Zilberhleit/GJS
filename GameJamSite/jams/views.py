import os

from django.http import HttpRequest, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from jams.models import GameJams, UploadFile, RatingUserJam
from users.models import User


class GameJamsLists(ListView):
    template_name = 'pages/jams_pages/jams.html'
    context_object_name = "jams_list"
    queryset = GameJams.objects.all()


class GameJamDetail(DetailView):
    model = GameJams
    template_name = 'pages/jams_pages/gamejam_detail.html'
    context_object_name = "gamejam_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        already_checked_users = []
        already_checked_games = []
        for game in UploadFile.objects.filter(jam_uuid=self.object.uuid).order_by('-uploaded_time'):
            if game.user.id not in already_checked_users:
                already_checked_users.append(game.user.id)
                already_checked_games.append(game)
        context["user_games"] = already_checked_games
        return context

    def get_object(self, queryset=None):
        return GameJams.objects.get(uuid=self.kwargs.get("uuid"))


def game_jam_upload(request, uuid):
    if request.method == "POST":
        if "game" in request.FILES:
            game_file = request.FILES["game"]
            game_extension = '.zip'
            if game_extension in game_file.name:
                instance = UploadFile.objects.update_or_create(file=game_file,
                                                     jam_uuid=get_object_or_404(GameJams, uuid=uuid),
                                                     user=get_object_or_404(User, username=request.user))
                return redirect("jams_list")
        return HttpResponseNotFound(render(request, "pages/errors/404.html"))


def game_jam_download(request, id, uuid):
    file_instance = get_object_or_404(UploadFile, id=id, jam_uuid=uuid, user=request.user)
    path = file_instance.file.path

    with open(path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_instance.file.name)}'
        return response


def count_stars(request, uuid, id):
    if request.method == "POST":
        if 'stars' in request.POST:
            instance = RatingUserJam.objects.update_or_create(jam_uuid=get_object_or_404(GameJams,
                                                                                         uuid=uuid),
                                                              user=get_object_or_404(User, id=id),
                                                              user_who_rate=get_object_or_404(User, id=request.user.id),
                                                              defaults={'stars': request.POST["stars"]})
            return redirect('gamejam_detail', uuid=uuid)
        return HttpResponseNotFound(render(request, "pages/errors/404.html"))


def handler404(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(render(request, "pages/errors/404.html"))
