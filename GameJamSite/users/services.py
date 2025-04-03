from django.db.models import Avg, Case, When, FloatField
from django.db.models.functions import Round

from jams.models import GameJam
from jams.models.game import Game


def get_user_jams_history(username: str):
    """ Получение истории джемов  """
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


def upload_photo(photo_type, request_files, user):
    """ Установка фото пользователя (аватар или шапка) """
    photo = request_files[photo_type]
    if is_valid_photo(photo):

        setattr(user, photo_type, photo)

        user.save()
        return user

def is_valid_photo(photo):
    """ Проверка фото пользователя (аватар или шапка) """
    return photo is not None and (photo.content_type == 'image/jpeg' or
            photo.content_type == 'image/png' or photo.content_type == 'image/jpg' or
            photo.content_type == 'image/webp' or photo.content_type == 'image/jfif') and photo.size <=  3 * 1024 * 1024