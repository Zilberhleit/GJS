from django.db import models
from jams.models import GameJam


class Question(models.Model):
    question_text = models.CharField(max_length=1000)
    count = models.IntegerField(default=0)
    jam_uuid = models.ForeignKey(GameJam, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question_text + " - " + self.jam_uuid.title + ' - ' + str(self.count)
