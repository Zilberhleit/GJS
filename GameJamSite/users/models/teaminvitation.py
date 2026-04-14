from django.conf import settings
from django.db import models

from .team import Team
from .user import User


class TeamInvitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="invitations")
    invitee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_invites"
    )
    inviter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_invites"
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Ожидает"),
            ("accepted", "Принято"),
            ("reject", "Отклонено"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Приглашение от {self.inviter.username} для {self.invitee.username}"
