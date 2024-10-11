from django.urls import path
from . import views


urlpatterns = [
    path('', views.GameJamsLists.as_view(), name='jams_list'),
    path('<uuid:uuid>/', views.GameJamDetail.as_view(), name='gamejam_detail')
]
