import uuid
from django.db import models
from django.conf import settings
from users.models import User


class GameJams(models.Model):
    jam_status = [
        ("FN", "Завершён"),
        ("OG", "Идёт"),
        ("PR", "Подготовка")
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    theme = models.CharField(max_length=255)
    status = models.CharField(max_length=3, choices=jam_status)
    winner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_winner",
                                  on_delete=models.SET_NULL, blank=True, null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users",
                                   blank=True)


class UploadFile(models.Model):
    file = models.FileField(upload_to="zip_uploads/")
    uploaded_time = models.DateTimeField(auto_now_add=True)
    jam_uuid = models.ForeignKey(GameJams, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
