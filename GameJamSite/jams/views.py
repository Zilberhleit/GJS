import os

from django.db.models import Avg
from django.http import HttpRequest, HttpResponseNotFound, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
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
        context["user_games"] = UploadFile.objects.filter(jam_uuid=self.object.uuid).order_by('-uploaded_time')

        if self.object.status == 'FN':
            context["user_avg_rating"] = count_final_rating(self.object.uuid)

        return context

    def get_object(self, queryset=None):
        return GameJams.objects.get(uuid=self.kwargs.get("uuid"))


def count_final_rating(uuid):
    return (RatingUserJam.objects.filter(jam_uuid_id=uuid).values('user__username')
            .annotate(avg_rating=Avg('stars')))


def game_jam_upload(request, uuid):
    if request.method == "POST":
        if "game" in request.FILES:
            game_file = request.FILES["game"]
            game_extension = '.zip'

            if game_file.name.endswith(game_extension):
                jam = get_object_or_404(GameJams, uuid=uuid)
                prev_game = UploadFile.objects.filter(
                    jam_uuid=jam,
                    user=request.user
                )

                if prev_game.exists():
                    prev_game.update(file=game_file)
                else:
                    UploadFile.objects.create(
                        file=game_file,
                        jam_uuid=jam,
                        user=request.user
                    )

                return redirect(reverse("gamejam_detail", kwargs={'uuid': uuid}))

        raise Http404


def game_jam_download(request, id, uuid):
    file_instance = get_object_or_404(UploadFile, id=id, jam_uuid=uuid)
    path = file_instance.file.path

    with open(path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_instance.file.name)}'
        return response


def count_stars(request, uuid, id):
    if request.method == "POST" and 'stars' in request.POST:
        RatingUserJam.objects.update_or_create(jam_uuid=get_object_or_404(GameJams,
                                                                          uuid=uuid),
                                               user=get_object_or_404(User, id=id),
                                               user_who_rate=get_object_or_404(User, id=request.user.id),
                                               defaults={'stars': request.POST["stars"]})
        return redirect('gamejam_detail', uuid=uuid)
    raise Http404


def home_page(request):
    return render(request, 'pages/index.html')

def handler404(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(render(request, "pages/errors/404.html"))
