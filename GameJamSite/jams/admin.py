from django.contrib import admin
from jams.models import GameJams, UploadFile, RatingUserJam

admin.site.register(GameJams)
admin.site.register(UploadFile)
admin.site.register(RatingUserJam)