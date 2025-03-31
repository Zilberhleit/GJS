from django.db import models
from users.models import User
from jams.models import GameJam


class RatingUserJam(models.Model):
    """ Модель рейтинга игр джема """
    jam_uuid = models.ForeignKey(GameJam, on_delete=models.CASCADE, verbose_name="Джем")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rated_user", verbose_name="Пользователь")
    user_who_rate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_rate", verbose_name="Кто оценил")
    stars = models.IntegerField(blank=True, verbose_name="Оценка")

    class Meta:
        verbose_name = "Рейтинг джема"
        verbose_name_plural = "Рейтинги джемов"

    def __str__(self):
        return str(self.jam_uuid) + ' | ' + str(self.user) + ' rated by ' + str(self.user_who_rate) + ' - ' + str(self.stars)
