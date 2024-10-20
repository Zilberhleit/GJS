from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=1000)
    count = models.IntegerField()