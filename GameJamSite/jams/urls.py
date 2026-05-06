from django.urls import path
from jam_polls import views as poll_view

from jams.views import MyGameJams

from . import views

urlpatterns = [
    path("", views.GameJamsLists.as_view(), name="jams_list"),
    path("app/", views.react_app, name="react_app"),
    path("my_jams/", MyGameJams.as_view(), name="my_jams"),
    path("<uuid:uuid>/", views.GameJamDetail.as_view(), name="gamejam_detail"),
    path("<uuid:uuid>/upload/", views.game_jam_upload, name="upload-game"),
    path("<uuid:uuid>/stars/<int:id>/", views.rate_game, name="count_stars"),
    path(
        "<uuid:uuid>/download/<slug:slug>/",
        views.game_jam_download,
        name="download_file",
    ),
    path("<uuid:uuid>/poll/", poll_view.PollList.as_view(), name="poll"),
    path("<uuid:uuid>/poll/submit/", poll_view.submit_poll, name="submit"),
    path("<uuid:uuid>/join_jam/", views.join_gamejam, name="join_gamejam"),
    path("<uuid:uuid>/leave_jam/", views.leave_gamejam, name="leave_gamejam"),
    path(
        "<uuid:uuid>/join_jam_team/<int:team_id>",
        views.join_jam_team,
        name="join_jam_team",
    ),
    path(
        "<uuid:uuid>/leave_jam_team/<int:team_id>",
        views.leave_jam_team,
        name="leave_jam_team",
    ),
    path("<uuid:uuid>/games/<slug:slug>/", views.jam_game_page, name="jam_game_page"),
]
