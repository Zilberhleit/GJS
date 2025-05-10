import os

from django.db import models
from django.utils.text import slugify


from jams.models import GameJam
from users.models import User


class Game(models.Model):
    """ Модель игры """
    title = models.CharField(max_length=100, verbose_name='Название игры')
    slug = models.SlugField(blank=True)
    description = models.TextField(verbose_name='Описание игры', blank=True, null=True)
    image = models.ImageField(upload_to="game_images/", verbose_name='Изображение игры', blank=True, null=True)

    jam_uuid = models.ForeignKey(GameJam, on_delete=models.CASCADE, related_name="games", verbose_name='Джем')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    game_file = models.FileField(upload_to="zip_uploads/", verbose_name='Файл игры')
    uploaded_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    def __str__(self):
        return self.title + " - " + self.jam_uuid.title + ' - ' + self.uploaded_time.strftime("%d.%m.%Y %H:%M:%S") + \
            ' - added by ' + self.user.username

    def save(self, *args, **kwargs):
        if not self.title and self.game_file:
            self.title = os.path.splitext(os.path.basename(self.game_file.name))[0]
        if self.slug is not None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
