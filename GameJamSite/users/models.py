from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")


class UploadFile(models.Model):
    file = models.FileField(upload_to="zip_uploads/")
    uploaded_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name