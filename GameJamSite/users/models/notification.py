from tabnanny import verbose

from django.conf import settings
from django.db import models

from .team import Team
from .user import User


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("team_invite", "Приглашение в команду"),
        ("team_accept", "Принятие приглашения"),
        ("team_reject", "Отклонение приглашения"),
    ]

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_notifications"
    )
    notification_type = models.CharField(
        max_length=100, choices=NOTIFICATION_TYPES, default="team_invite"
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Приглашение от {self.sender.username} для {self.recipient.username}"
