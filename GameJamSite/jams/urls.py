from django.urls import path
from . import views
from jam_polls import views as poll_view

urlpatterns = [
    path('', views.GameJamsLists.as_view(), name='jams_list'),
    path('<uuid:uuid>/', views.GameJamDetail.as_view(), name='gamejam_detail'),
    path('<uuid:uuid>/upload', views.game_jam_upload, name='upload-game'),
    path('<uuid:uuid>/download/<int:id>/', views.game_jam_download, name='download_file'),
    path('<uuid:uuid>/poll/', poll_view.PollList.as_view(), name='poll')
]
