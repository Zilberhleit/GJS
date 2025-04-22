import random
from datetime import timedelta

from django.contrib import admin

from jams.models import GameJam, Game, RatingUserJam
from jams.utils import rand_date


class GameJamAdmin(admin.ModelAdmin):
    actions = ('set_actual_start_and_end_dates',)

    @admin.action(description='Change Start Date')
    def set_actual_start_and_end_dates(self, request, queryset):
        """  Action для генерации случайных дат """
        for gamejam in queryset:
            if gamejam.status == 'PR' or gamejam.status == 'OG':
                gamejam.date_start = rand_date()
                gamejam.date_end = gamejam.date_start + timedelta(days=random.randint(3, 14))
                gamejam.save()
        self.message_user(request, "Start date updated successfully.")


admin.site.register(GameJam, GameJamAdmin)
admin.site.register(Game)
admin.site.register(RatingUserJam)
