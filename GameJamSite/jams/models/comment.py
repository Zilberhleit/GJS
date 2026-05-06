from django.db import models
from users.models import Post, User

# from jams.models import Game


class Comment(models.Model):
    game_id = models.ForeignKey(
        "Game",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="game",
        verbose_name="Игра",
    )
    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="post",
        verbose_name="Пост",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="автор комментария"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
