from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Team
from users.models.team import TeamMembership


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Team)
admin.site.register(TeamMembership)
