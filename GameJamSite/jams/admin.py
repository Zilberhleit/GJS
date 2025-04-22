import os
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


class GameAdmin(admin.ModelAdmin):
    actions = ('set_slug', 'set_title',)

    @admin.action(description="Задать слаг играм")
    def set_slug(self, request, queryset):
        for game in queryset:
            game.prepopulated_fields = {'slug': ('title',)}
            game.save()

    @admin.action(description="Задать имя игре")
    def set_title(self, request, queryset):
        for game in queryset:
            game.title = os.path.splitext(os.path.basename(game.game_file.name))[0]
            game.save()


admin.site.register(GameJam, GameJamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(RatingUserJam)
