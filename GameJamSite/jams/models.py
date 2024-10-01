from django.db import models

class GameJams (models.Model):
    title = models.CharField(max_length=255)
    date_start = models.DateTimeField("start jam")
    date_end = models.DateTimeField("end jam")
    theme = models.TextField()
    jam_slug = models.SlugField(
        max_length=255, db_index=True, unique=True, verbose_name="URL"
    )
