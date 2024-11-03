from django.urls import path
from users import views

urlpatterns = [
    path('<str:nickname>/', views.Profile.as_view(), name='profile_detail'),
    path('gamelist/', views.GameList.as_view(), name='game_list')
]
