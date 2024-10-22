from django.urls import path
from users import views

urlpatterns = [
    path('', views.Profile.as_view(), name='profile_detail'),
    path('', views.GameList.as_view(), name='game_list')
]
