from django.db import models
from jams.models import Game

from users.models import User


class Comment(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="comments", verbose_name="комментарий")
    name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор комментария")
    body = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
