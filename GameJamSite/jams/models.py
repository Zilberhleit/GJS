import uuid
from django.conf import settings
from django.db import models
from users.models import User


class GameJams(models.Model):
    jam_status = [
        ("FN", "Завершён"),
        ("OG", "Идёт"),
        ("PR", "Подготовка")
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='Название джема')
    date_start = models.DateTimeField(verbose_name='Дата начала')
    date_end = models.DateTimeField(verbose_name='Дата окончания')
    theme = models.CharField(max_length=255, verbose_name='Тема')
    status = models.CharField(max_length=3, choices=jam_status, verbose_name='Статус')
    winner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_winner",
                                  on_delete=models.SET_NULL, blank=True, null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users",
                                   blank=True)

    def __str__(self):
        return self.title + " - " + self.theme

class UploadFile(models.Model):
    file = models.FileField(upload_to="zip_uploads/")
    uploaded_time = models.DateTimeField(auto_now_add=True)
    jam_uuid = models.ForeignKey(GameJams, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name


class RatingUserJam(models.Model):
    jam_uuid = models.ForeignKey(GameJams, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rated_user")
    user_who_rate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_rate")
    stars = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.jam_uuid) + " - " + str(self.user)