import mimetypes
import os
import urllib.parse
from ast import Continue
from types import NoneType
from uuid import UUID

from django.db.models import Avg, Count, F, Q, Window
from django.db.models.functions import Rank, RowNumber
from django.http import (
    FileResponse,
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from users.models import User

from jams.models import Game, GameJam, RatingUserJam

from .filters import GameJamsFilter
from .services import get_file_mime_type, is_valid_game_file, is_valid_image_file


class GameJamsLists(ListView):
    """Представление списка геймджемов"""

    template_name = "pages/jams_pages/jams.html"
    queryset = GameJam.objects.order_by("-status", "-date_start")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = GameJamsFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context


class MyGameJams(ListView):
    """Список геймджемов пользователя"""

    template_name = "pages/jams_pages/jams.html"

    def get_queryset(self):
        return GameJam.objects.filter(author=self.request.user).order_by(
            "-status", "-date_start"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = GameJamsFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context


class GameJamDetail(DetailView):
    """Представление просмотра деталей конкретного геймджема"""

    model = GameJam
    template_name = "pages/jams_pages/gamejam_detail.html"

    def get_object(self, queryset=None):
        return GameJam.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_games = (
            Game.objects.filter(jam_uuid=self.object.uuid)
            .annotate(
                avg_rating=Avg(
                    "user__rated_user__stars",
                    filter=Q(user__rated_user__jam_uuid=self.object),
                ),
            )
            .annotate(
                place=Window(
                    expression=RowNumber(),
                    order_by=F("avg_rating").desc(nulls_last=True),
                )
            )
            .order_by("-avg_rating")
        )

        context["user_games"] = user_games
        if self.request.user.is_authenticated:
            current_user_game = next(
                (game for game in user_games if game.user_id == self.request.user.id),
                None,
            )
            if current_user_game:
                context["current_user_game"] = current_user_game

        return context


def get_object(self, queryset=None):
    return GameJam.objects.get(uuid=self.kwargs.get("uuid"))


def count_jam_rating(uuid: UUID):
    """Функция подсчета рейтинга геймджема"""
    return (
        RatingUserJam.objects.filter(jam_uuid_id=uuid)
        .values("user__username", "user__id")
        .annotate(avg_rating=Avg("stars"))
    )


def game_jam_upload(request, uuid: UUID):
    """Представление для загрузки игры"""
    if request.method == "POST":
        fields_to_check = (
            "jam_uuid",
            "title",
            "description",
        )
        if "game_file" in request.FILES and all(
            field in request.POST for field in fields_to_check
        ):
            title = request.POST["title"]
            description = request.POST["description"]
            game_file = request.FILES["game_file"]
            image_file = request.FILES.get("image", None)

            if is_valid_game_file(game_file) and (
                image_file is None or is_valid_image_file(image_file)
            ):
                jam = get_object_or_404(GameJam, uuid=uuid)
                prev_game = Game.objects.filter(jam_uuid__uuid=uuid, user=request.user)
                # Заметка: надо посмотреть как правильно заменять файлы,
                # ибо это может вести к переполнению одинаковыми файлами
                if prev_game.exists():
                    updated_game = prev_game.first()
                    updated_game.title = title
                    updated_game.description = description
                    updated_game.image = image_file
                    updated_game.game_file = game_file
                    updated_game.save()
                else:
                    Game.objects.create(
                        title=title,
                        description=description,
                        image=image_file,
                        game_file=game_file,
                        jam_uuid=jam,
                        user=request.user,
                    )

                return redirect(reverse("gamejam_detail", kwargs={"uuid": uuid}))

        raise Http404


def game_jam_download(request, uuid: UUID, slug):
    """Представление для скачивания игры"""
    file_instance = get_object_or_404(Game, jam_uuid=uuid, slug=slug)
    path = file_instance.game_file.path
    filename = file_instance.game_file.name

    content_type = get_file_mime_type(path, filename)

    response = FileResponse(open(path, "rb"), content_type=content_type)
    filename_encoded = urllib.parse.quote(filename)

    response["Content-Disposition"] = (
        f'attachment; filename="{os.path.basename(filename_encoded)}"'
    )
    response["Content-Length"] = os.path.getsize(path)
    # with open(path, "rb") as fh:
    #     response = HttpResponse(fh.read(), content_type="application/force-download")
    #     response["Content-Disposition"] = (
    #         f'attachment; filename="{os.path.basename(filename)}"'
    #     )
    return response


def rate_game(request, uuid: UUID, id: int):
    """Представление для рейтинга игры"""
    if request.method == "POST" and "stars" in request.POST:
        RatingUserJam.objects.update_or_create(
            jam_uuid=get_object_or_404(GameJam, uuid=uuid),
            user=get_object_or_404(User, id=id),
            user_who_rate=get_object_or_404(User, id=request.user.id),
            defaults={"stars": request.POST["stars"]},
        )
        return redirect("gamejam_detail", uuid=uuid)
    raise Http404


def join_gamejam(request, uuid: UUID):
    """Присоединение пользователя к джему"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    gamejam = GameJam.objects.get(uuid=uuid)
    gamejam.users.add(request.user)
    return redirect("gamejam_detail", uuid=uuid)


def leave_gamejam(request, uuid: UUID):
    """Уход пользователя из геймджема"""
    gamejam = GameJam.objects.get(uuid=uuid)

    if request.user in gamejam.users.all():
        gamejam.users.remove(request.user)
    return redirect("gamejam_detail", uuid=uuid)


def home_page(request):
    """Представление для главной страницы"""
    return render(request, "pages/index.html")


def game_page(request, uuid, slug):
    game = Game.objects.get(jam_uuid=uuid, slug=slug)
    return render(request, "pages/jams_pages/game_page.html", {"game": game})


def games_page(request):
    return render(request, "pages/jams_pages/games.html")


def handler404(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(render(request, "pages/errors/404.html"))
