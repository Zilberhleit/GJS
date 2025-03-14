from django.contrib.auth import get_user_model
from django.db.models import Avg, Case, When, FloatField
from django.db.models.functions import Round

from jams.models import GameJams


def get_user_jams_history(user: get_user_model()):
    return (GameJams.objects.filter(users=user, status='FN')
    .annotate(
        user_rating=Round(
            Avg(
                Case(
                    When(ratinguserjam__user=user, then='ratinguserjam__stars'),
                    output_field=FloatField()
                )
            ),
            1  # Округляем до 1 знака после запятой
        )
    )).exclude(user_rating=None)