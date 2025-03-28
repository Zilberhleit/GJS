from django.contrib import admin
from jam_polls.models import GameJamTheme, ThemeVote, Theme

admin.site.register(GameJamTheme)
admin.site.register(ThemeVote)
admin.site.register(Theme)

