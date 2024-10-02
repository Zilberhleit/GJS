from django.urls import path
from . import views


urlpatterns = [
    path('jams/', views.jam_list_views),
]
