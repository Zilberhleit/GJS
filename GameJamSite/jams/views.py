import os
from uuid import UUID

from django.db.models import Avg
from django.http import HttpRequest, HttpResponseNotFound, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from jams.models import GameJam, RatingUserJam, Game
from users.models import User
from .filters import GameJamsFilter


class GameJamsLists(ListView):
    """ Представление списка геймджемов """
    template_name = 'pages/jams_pages/jams.html'
    queryset = GameJam.objects.order_by('-status', '-date_start')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = GameJamsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class GameJamDetail(DetailView):
    """ Представление просмотра деталей конкретного геймджема """
    # ну что пайтонисты как там без инкапсуляции?
    model = GameJam
    template_name = 'pages/jams_pages/gamejam_detail.html'
    context_object_name = "gamejam_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_games = Game.objects.filter(jam_uuid=self.object.uuid).order_by('-uploaded_time')
        for game in user_games:
            game.cleaned_name = game.game_file.name.replace('zip_uploads/', '')

        context["user_games"] = user_games

        if self.object.status == 'FN':
            context["final_rating"] = {}

            final_rating = count_final_rating(self.object.uuid)

            if self.request.user.is_authenticated:
                current_user_rating = final_rating.filter(user=self.request.user)

                if current_user_rating.exists():
                    context["final_rating"]['current_user_rating'] = current_user_rating[0]

                context["final_rating"]['all_rating'] = (final_rating
                                                         .difference(current_user_rating)
                                                         .order_by('-avg_rating'))
            else:
                context["final_rating"]['all_rating'] = final_rating.order_by('-avg_rating')

        return context

    def get_object(self, queryset=None):
        return GameJam.objects.get(uuid=self.kwargs.get("uuid"))


def count_final_rating(uuid: UUID):
    """ Функция подсчета рейтинга геймджема """
    return (RatingUserJam.objects.filter(jam_uuid_id=uuid).values('user__username', 'user__id')
            .annotate(avg_rating=Avg('stars')))


def game_jam_upload(request, uuid: UUID):
    """ Представление для загрузки игры """
    if request.method == "POST":
        if "game" in request.FILES:
            game_file = request.FILES["game"]
            game_extension = '.zip'

            if game_file.name.endswith(game_extension):
                jam = get_object_or_404(GameJam, uuid=uuid)
                prev_game = Game.objects.filter(
                    jam_uuid=jam,
                    user=request.user
                )

                if prev_game.exists():
                    prev_game.update(
                        game_file=game_file,
                        title=os.path.splitext(os.path.basename(game_file.name))[0])
                else:
                    Game.objects.create(
                        game_file=game_file,
                        jam_uuid=jam,
                        user=request.user
                    )

                return redirect(reverse("gamejam_detail", kwargs={'uuid': uuid}))

        raise Http404


def game_jam_download(request, uuid: UUID, slug):
    """ Представление для скачивания игры """
    file_instance = get_object_or_404(Game, jam_uuid=uuid, slug=slug)
    path = file_instance.game_file.path

    with open(path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_instance.game_file.name)}'
        return response


def count_stars(request, uuid: UUID, id: int):
    """ Представление для рейтинга игры """
    if request.method == "POST" and 'stars' in request.POST:
        RatingUserJam.objects.update_or_create(jam_uuid=get_object_or_404(GameJam,
                                                                          uuid=uuid),
                                               user=get_object_or_404(User, id=id),
                                               user_who_rate=get_object_or_404(User, id=request.user.id),
                                               defaults={'stars': request.POST["stars"]})
        return redirect('gamejam_detail', uuid=uuid)
    raise Http404


def home_page(request):
    """ Представление для главной страницы """
    return render(request, 'pages/index.html')


def game_page(request, uuid, slug):
    game = Game.objects.get(
        jam_uuid=uuid,
        slug=slug
    )
    game.cleaned_name = game.game_file.name.replace('zip_uploads/', '')
    return render(request, 'pages/jams_pages/game_page.html', {'game': game})


def handler404(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(render(request, "pages/errors/404.html"))
