from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from jams import views
from users import views as users_view

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("admin/", admin.site.urls),
    path("jams/", include("jams.urls")),
    path("games/", views.games_page, name="games"),
    path("login/", users_view.login_view, name="login"),
    path("logout/", users_view.logout_view, name="logout"),
    path("register/", users_view.RegisterUser.as_view(), name="regist"),
    path("profile/", include("users.urls")),
    path("accounts/", include("allauth.urls")),
    path("about/", users_view.about_page, name="about"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.handler404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
