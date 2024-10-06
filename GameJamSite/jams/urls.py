from django.urls import path
from . import views


urlpatterns = [
    path('', views.jam_list_views, name='jams'),
    path('event/<uuid:jam_num>', views.jam_event_view, name='event')
]
