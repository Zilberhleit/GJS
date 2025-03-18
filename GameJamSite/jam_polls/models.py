from django.db import models
from jams.models import GameJam
from django.conf import settings

class GameJamTheme(models.Model):
    theme = models.CharField(max_length=255, verbose_name="Тема")
    gamejam = models.ForeignKey(GameJam, on_delete=models.CASCADE, verbose_name="Джем")

    class Meta:
        verbose_name = "Тема джема"
        verbose_name_plural = "Темы джема"

    def __str__(self):
        return self.theme + " - " + self.gamejam.title

class ThemeVote(models.Model):
    vote = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    theme = models.ForeignKey(GameJamTheme, on_delete=models.CASCADE, verbose_name="Тема джема")

    class Meta:
        verbose_name = "Голосование за тему"
        verbose_name_plural = "Голосования за тему"

    def __str__(self):
        return str(self.user) + " проголосовал " + str(self.vote) + " за "  + str(self.theme)

