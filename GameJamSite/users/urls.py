from django.urls import path
from users import views

urlpatterns = [
    path('<str:username>/', views.Profile.as_view(), name='profile_detail')
]
