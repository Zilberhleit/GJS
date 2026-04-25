from tabnanny import verbose

from django.conf import settings
from django.db import models
from django_prose_editor.fields import ProseEditorField
from django_prose_editor.sanitized import SanitizedProseEditorField

from .user import User


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    excerpt = ProseEditorField()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
