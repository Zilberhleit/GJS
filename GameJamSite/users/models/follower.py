from django.contrib.auth.models import AbstractUser
from django.db import models

from .user import User


class Follower(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following_relations"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower_relations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ["follower", "following"]

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
