from django.db import models
from jams.models import GameJam
from django.conf import settings

class Poll(models.Model):
    question_text = models.CharField(max_length=1000)
    total_votes = models.IntegerField(default=0)
    jam_uuid = models.ForeignKey(GameJam, on_delete=models.CASCADE)
    users_who_voted = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users_who_voted", null=True, blank=True, verbose_name='Кто проголосовал')


    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question_text + " - " + self.jam_uuid.title + ' - ' + str(self.total_votes)
