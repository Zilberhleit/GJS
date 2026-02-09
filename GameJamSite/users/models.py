from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Модель пользователя """
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    avatar_image = models.ImageField(upload_to="users", blank=True, null=True)
    hat_image = models.ImageField(upload_to="users", blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name="Подписчики")

# Реализовать систему подписок Follow System, реализовать динамическую смену через JS
class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name="following_relations")
    following = models.ForeignKey(User, on_delete=models.CASCADE, 
                                  related_name="follower_relations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together=['follower','following']

    def __str__(self):
            return f"{self.follower.username} follows {self.followed.username}"