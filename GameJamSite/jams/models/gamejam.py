import uuid

from django.conf import settings
from django.db import models



class GameJam(models.Model):
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
    status = models.CharField(max_length=3, choices=jam_status, default="PR", verbose_name='Статус')
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_winner",
                               on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Победитель')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users",
                                   blank=True, verbose_name='Участники')
    class Meta:
        verbose_name = "Геймджем"
        verbose_name_plural = "Геймджемы"

    def __str__(self):
        return self.title + " - " + self.theme

