from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from jams import views
from users import views as users_view
from users.users_views import (
    add_comment_to_post,
    create_post,
    delete_comment,
    delete_post,
    edit_post,
    post_detail,
    posts_page,
)

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("admin/", admin.site.urls),
    path("jams/", include("jams.urls")),
    path("games/", views.GamesLists.as_view(), name="games"),
    path("login/", users_view.login_view, name="login"),
    path("logout/", users_view.logout_view, name="logout"),
    path("register/", users_view.RegisterUser.as_view(), name="regist"),
    path("profile/", include("users.urls")),
    path("accounts/", include("allauth.urls")),
    path("md-editor/", include("django_markdown_widget.urls")),
    path("about/", users_view.about_page, name="about"),
    path("create_jam", users_view.create_jam, name="create_jam"),
    path("create_team", users_view.create_team, name="create_team"),
    path("create_post", create_post, name="create_post"),
    path("edit_post/<int:post_id>", edit_post, name="edit_post"),
    path("team/<int:team_id>/post/create/", create_post, name="create_team_post"),
    path("delete_post/<int:post_id>", delete_post, name="delete_post"),
    path("team/<int:id>", users_view.team_detail, name="team_detail"),
    path("team/<int:id>/invite/", users_view.invite_to_team, name="invite_to_team"),
    path("post/<int:post_id>", post_detail, name="post_detail"),
    path("posts/", posts_page, name="posts"),
    path(
        "comment/post/<int:post_id>/add/",
        add_comment_to_post,
        name="add_comment_to_post",
    ),
    path(
        "delete_comment/<int:comment_id>",
        delete_comment,
        name="delete_comment",
    ),
    path("notifications/", users_view.notifications, name="notifications"),
    path("api/search-users/", users_view.search_users, name="search_users"),
    path("api/notifications/", users_view.get_notifications, name="api_notifications"),
    path(
        "api/notifications/<int:notification_id>/read/",
        users_view.notification_read,
        name="api_notification_read",
    ),
    path(
        "api/notifications/<int:team_id>/accept/",
        users_view.accept_invite,
        name="accept_invite",
    ),
    path(
        "api/notifications/<int:team_id>/reject/",
        users_view.reject_invite,
        name="reject_invite",
    ),
    path("game/<slug:slug>/", views.game_page, name="game_page"),
    path("game/<slug:slug>/download/", views.game_download, name="download_game"),
    path("my_games/", views.MyGames.as_view(), name="my_games"),
    path("create_game/", users_view.create_game, name="create_game"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.handler404
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
