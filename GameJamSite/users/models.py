from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    avatar_image = models.ImageField(upload_to="users", blank=True, null=True)
    hat_image = models.ImageField(upload_to="users", blank=True, null=True)
