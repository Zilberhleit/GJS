from django.contrib import admin
from django.urls import path

from jams import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jams/', views.jam_list_views),
    path('load/', views.jam_load)
]
