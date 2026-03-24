from tabnanny import verbose

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    avatar_image = models.ImageField(upload_to="users", blank=True, null=True)
    hat_image = models.ImageField(upload_to="users", blank=True, null=True)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="Подписчики"
    )
    strikes = models.IntegerField(default=0, verbose_name="Нарушения")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")
