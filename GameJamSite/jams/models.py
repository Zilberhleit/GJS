import uuid
from django.db import models
from django.conf import settings


class GameJams(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    theme = models.CharField(max_length=255)
    winner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_winner",
                                  on_delete=models.SET_NULL, blank=True, null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users",
                                   blank=True)
