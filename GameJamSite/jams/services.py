import mimetypes
import os
import tempfile

import magic
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django_clamd.validators import validate_file_infection

from jams.models import Game, RatingUserJam


def get_user_ratings(rated_user, rater, uuid):
    return RatingUserJam.objects.filter(
        jam_uuid=uuid, user=rated_user, user_who_rate=rater
    )


def is_virus_free(game_file: UploadedFile) -> bool:
    """Проверка на вирусы через ClamAV"""
    try:
        validate_file_infection(game_file)
        print("is_virus_free validate success")
        return True
    except ValidationError:
        print("is_virus_free validate failed")
        return False


def is_valid_game_file(game_file: UploadedFile) -> bool:
    """Проверка файла игры пользователя (.rar или .zip)

    :param game_file: загруженный файл игры пользователя

    :return: True, если файл имеет расширение .rar или .zip, иначе False
    """

    try:
        if not is_virus_free(game_file):
            print("is_valid_game_file not virus free")
            return False
    except Exception as e:
        print(f"ClamAV проверка недоступна: {e}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        for chunk in game_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    game_extensions = (".zip", ".rar")
    if not any(game_file.name.lower().endswith(ext) for ext in game_extensions):
        print("not right ext")
        return False

    try:
        mime = magic.from_file(tmp_path, mime=True)
    finally:
        os.unlink(tmp_path)

    game_file.seek(0)

    allowed_mimes = [
        "application/zip",
        "application/x-zip-compressed",
        "application/x-rar-compressed",
        "application/vnd.rar",
    ]

    if mime in allowed_mimes:
        return True
    else:
        print(mime)
        print("mimes is invalid")
        return False


def is_valid_image_file(image_file: UploadedFile) -> bool:
    """Проверка фото для игры от пользователя

    :param image_file: фото пользователя (которое устанавливается для страницы игры)

    :return: True, если соответствует расширению, иначе False
    """
    image_extensions = (".jpg", ".png", ".jpeg", "webp", "jfif")
    return any(image_file.name.endswith(ext) for ext in image_extensions)


def get_file_mime_type(path: str, filename: str) -> str:
    """Получение MIME-типа для скачиваения файла со страницы

    :param path: путь для определения существования объекта
    :param filename: имя файла, для определения типа

    :return: Строка для определения формата файла
    """
    if "zip_uploads" not in path:
        print("path is not right", filename)
        # Заметка: не самое красивое решение,
        # нужно "внедрять" подпапку а не писать новый путь
        path = f"/app/media/zip_uploads/{filename}"

    if not os.path.exists(path):
        return "Nan"

    content_type, encoding = mimetypes.guess_type(path)
    if content_type is None:
        if filename.endswith(".zip"):
            content_type = "application/zip"
        elif filename.endswith(".rar"):
            content_type = "application/rar"
        else:
            content_type = "application/octet-stream"

    return content_type
