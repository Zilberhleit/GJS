from tabnanny import verbose

from django.conf import settings
from django.db import models
from django_markdown_widget import MarkdownCleanupMixin
from django_prose_editor.fields import ProseEditorField
from django_prose_editor.sanitized import SanitizedProseEditorField

from .team import Team
from .user import User


class Post(MarkdownCleanupMixin, models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    markdown_cleanup_fields = ["content"]

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
