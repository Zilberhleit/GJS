import mimetypes
import os

import magic
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django_clamd.validators import validate_file_infection

from jams.models import Game


def is_virus_free(game_file: UploadedFile) -> bool:
    """Проверка на вирусы через ClamAV"""
    try:
        validate_file_infection(game_file)
        return True
    except ValidationError:
        return False


def is_valid_game_file(game_file: UploadedFile) -> bool:
    """Проверка файла игры пользователя (.rar или .zip)

    :param game_file: загруженный файл игры пользователя

    :return: True, если файл имеет расширение .rar или .zip, иначе False
    """
    game_extensions = (".zip", ".rar")
    if not any(game_file.name.lower().endswith(ext) for ext in game_extensions):
        return False

    mime = magic.from_buffer(game_file.read(1024), mime=True)
    game_file.seek(0)

    allowed_mimes = [
        "application/zip",
        "application/x-zip-compressed",
        "application/x-rar-compressed",
        "application/vnd.rar",
    ]

    try:
        if not is_virus_free(game_file):
            return False
    except Exception as e:
        print(f"ClamAV проверка недоступна: {e}")

    return mime in allowed_mimes


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
