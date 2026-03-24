from tabnanny import verbose

from django.conf import settings
from django.db import models


class Team(models.Model):
    """Команды пользователей"""

    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.CharField(max_length=1000, blank=True, verbose_name="Описание")
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="team_users", verbose_name="Участники"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="team_creator",
        verbose_name="Создатель",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return self.name
