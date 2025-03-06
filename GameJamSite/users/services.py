from django.contrib.auth import get_user_model
from django.db.models import Avg, Subquery

from jams.models import GameJams, RatingUserJam


def get_user_past_jams_history(user: get_user_model()):
    jams_user_rating_subquery = RatingUserJam.objects.filter(user=user).annotate(
        total_rating=Avg('stars'))

    return (GameJams.objects.filter(users=user, status='FN').annotate(
        avg_rating=Subquery(jams_user_rating_subquery.values('total_rating')))
            .values('uuid', 'title', 'theme', 'winner', 'avg_rating'))
