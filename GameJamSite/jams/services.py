import mimetypes
import os

from django.core.files.uploadedfile import UploadedFile

from jams.models import Game


def is_valid_game_file(game_file: UploadedFile) -> bool:
    """Проверка файла игры пользователя (.rar или .zip)

    :param game_file: загруженный файл игры пользователя

    :return: True, если файл имеет расширение .rar или .zip, иначе False
    """
    game_extensions = (".zip", ".rar")
    return any(game_file.name.endswith(ext) for ext in game_extensions)


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
