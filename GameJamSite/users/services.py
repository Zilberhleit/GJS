from django.contrib.auth import get_user_model
from django.db.models import Avg, Case, When, FloatField
from django.db.models.functions import Round

from jams.models import GameJam
from jams.models.game import Game


def get_user_jams_history(username: str):
    return (GameJam.objects.filter(users__username=username, status='FN')
    .annotate(
        user_rating=Round(
            Avg(
                Case(
                    When(ratinguserjam__user__username=username, then='ratinguserjam__stars'),
                    output_field=FloatField()
                )
            ),
            1  # Округляем до 1 знака после запятой
        )
    )).exclude(user_rating=None).values('uuid', 'title', 'theme', 'user_rating')


def get_user_games_history(username: str):
    return Game.objects.filter(user__username=username)
