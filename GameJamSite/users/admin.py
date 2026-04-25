from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Team
from users.models.follower import Follower
from users.models.notification import Notification
from users.models.post import Post
from users.models.team import TeamMembership
from users.models.teaminvitation import TeamInvitation


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Team)
admin.site.register(TeamMembership)
admin.site.register(Notification)
admin.site.register(TeamInvitation)
admin.site.register(Post)
admin.site.register(Follower)
