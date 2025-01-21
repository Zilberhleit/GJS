from django.urls import path
from users import views

urlpatterns = [
    path('<str:username>/', views.Profile.as_view(), name='profile_detail'),
    path('<str:username>/redaction', views.redactor, name='redactor'),
    path('<str:username>/write_post', views.write_post, name='write_post')
]
