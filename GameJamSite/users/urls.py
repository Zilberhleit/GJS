from django.urls import path

from users import views

urlpatterns = [
    path("<str:username>/", views.Profile.as_view(), name="profile_detail"),
    path("<str:username>/redaction", views.redactor, name="redactor"),
    path(
        "<str:username>/upload_photo",
        views.upload_photo_view,
        name="upload-photo",
    ),
    # new URL
    path("<str:username>/follow", views.follow, name="follow"),
    path("<str:username>/unfollow", views.unfollow, name="unfollow"),
]
