from typing import Union

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Avg, Case, When, FloatField, QuerySet
from django.db.models.functions import Round
from django.utils.datastructures import MultiValueDict

from jams.models import GameJam
from jams.models.game import Game


def get_user_jams_history(username: str) -> QuerySet:
    """ Получение истории джемов

    :param username: Имя пользователя

    :return: История джемов

    """
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


def get_user_games_history(username: str) -> QuerySet:
    return Game.objects.filter(user__username=username)


def upload_photo(photo_type: str, request_files: MultiValueDict, user: get_user_model()) -> Union[
    get_user_model(), None]:
    """ Установка фото пользователя (аватар или шапка)

        :param photo_type: тип фото: 'avatar_image' или 'hat_image'
        :param request_files: переданные изображения
        :param user: пользователь загрузивший фото

        :return: Объект пользователя или None
    """
    photo = request_files[photo_type]

    if is_valid_photo(photo):
        setattr(user, photo_type, photo)

        user.save()
        return user


def is_valid_photo(photo: InMemoryUploadedFile) -> bool:
    """ Проверка фото пользователя (аватар или шапка)

    :param photo: фото пользователя (аватар или шапка)

    :return: True, если фото валидно, иначе False
    """
    return photo is not None and (photo.content_type == 'image/jpeg' or
                                  photo.content_type == 'image/png' or photo.content_type == 'image/jpg' or
                                  photo.content_type == 'image/webp' or photo.content_type == 'image/jfif') and photo.size <= 5 * 1024 * 1024
