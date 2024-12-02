from django.db import models
from jams.models import GameJams


class Question(models.Model):
    question_text = models.CharField(max_length=1000)
    count = models.IntegerField(default=0)
    jam_uuid = models.ForeignKey(GameJams, on_delete=models.CASCADE)

