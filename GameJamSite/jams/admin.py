import os

from django.contrib import admin
from jams.models import GameJam, Game, RatingUserJam


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


admin.site.register(GameJam)
admin.site.register(Game, GameAdmin)
admin.site.register(RatingUserJam)
