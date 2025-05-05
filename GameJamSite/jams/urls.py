from django.urls import path
from . import views
from jam_polls import views as poll_view

urlpatterns = [
    path('', views.GameJamsLists.as_view(), name='jams_list'),
    path('<uuid:uuid>/', views.GameJamDetail.as_view(), name='gamejam_detail'),
    path('<uuid:uuid>/upload/', views.game_jam_upload, name='upload-game'),
    path('<uuid:uuid>/stars/<int:id>/', views.count_stars, name='count_stars'),
    path('<uuid:uuid>/download/<slug:slug>/', views.game_jam_download, name='download_file'),
    path('<uuid:uuid>/poll/', poll_view.PollList.as_view(), name='poll'),
    path('<uuid:uuid>/poll/submit/', poll_view.submit_poll, name='submit'),
    path('<uuid:uuid>/games/<slug:slug>', views.game_page, name='game_page')
]
