import uuid
from tabnanny import verbose
from this import s

from django.conf import settings
from django.db import models
from users.models.team import Team

from jams.utils import (
    create_gamejam_change_status_periodic_task,
    update_gamejam_change_status_periodic_task,
)


class GameJam(models.Model):
    """Модель геймджема"""

    jam_status = [
        ("FN", "Завершён"),
        ("OG", "Идёт"),
        ("RT", "Оценка"),
        ("PR", "Подготовка"),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Название джема")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jam_author",
        verbose_name="Автор геймджема",
    )

    description = models.TextField(
        default="", blank=True, null=True, verbose_name="Описание джема"
    )
    date_start = models.DateTimeField(verbose_name="Дата начала")
    date_end = models.DateTimeField(verbose_name="Дата окончания")
    date_rating = models.DateTimeField(
        verbose_name="Дата оценивания", null=True, blank=True
    )
    theme = models.CharField(max_length=255, blank=True, verbose_name="Тема")
    image = models.ImageField(
        upload_to="jams/", blank=True, null=True, verbose_name="Изображение"
    )
    status = models.CharField(
        max_length=3, choices=jam_status, default="PR", verbose_name="Статус"
    )
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_winner",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Победитель",
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="users",
        blank=True,
        verbose_name="Участники",
    )
    teams = models.ManyToManyField(Team, blank=True, verbose_name="Команды участиники")
    has_poll = models.BooleanField(default=False, verbose_name="Есть голосование")

    class Meta:
        verbose_name = "Геймджем"
        verbose_name_plural = "Геймджемы"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old = None

        if not is_new:
            old = GameJam.objects.get(uuid=self.uuid)

        super().save(*args, **kwargs)

        if is_new:
            self._create_tasks()
        else:
            self._update_tasks(old)

    def _create_tasks(self):
        create_gamejam_change_status_periodic_task(self, "OG", self.date_start)
        create_gamejam_change_status_periodic_task(self, "FN", self.date_end)
        create_gamejam_change_status_periodic_task(self, "RT", self.date_rating)

    def _update_tasks(self, old):

        if self.date_start >= self.date_end:
            print("date start must be early than end")
            return
        if self.date_rating:
            if self.date_rating <= self.date_start:
                print("date rating must be later than start")
                return
            if self.date_rating >= self.date_end:
                print("date rating must be earlier than end")
                return

        if old.date_start != self.date_start:
            update_gamejam_change_status_periodic_task(self, "OG", self.date_start)
        if old.date_end != self.date_end:
            update_gamejam_change_status_periodic_task(self, "FN", self.date_end)
        if old.date_rating != self.date_rating:
            update_gamejam_change_status_periodic_task(self, "RT", self.date_rating)

    def __str__(self):
        return self.title + " - " + self.theme
