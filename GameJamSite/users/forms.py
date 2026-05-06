from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django_markdown_widget import MarkdownEditorWidget
from jams.models import Comment, Game
from jams.services import is_valid_game_file, is_valid_image_file

from .models import Post


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Написать комментарий...",
                    "class": "comment-textarea",
                }
            ),
        }
        labels = {
            "body": "",
        }


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ["title", "description", "image", "game_file"]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Опишите вашу игру...",
                    "class": "descr-textarea",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "game_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".zip,.rar,.7z",
                }
            ),
        }
        labels = {
            "title": "Название игры",
            "description": "Описание",
            "image": "Превью (изображение)",
            "game_file": "Файл игры (ZIP, RAR)",
        }

    def clean_game_file(self):
        if is_valid_game_file(self.cleaned_data.get("game_file")):
            return self.cleaned_data.get("game_file")

    def clean_image(self):
        if is_valid_image_file(self.cleaned_data.get("image")):
            return self.cleaned_data.get("image")


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "content": MarkdownEditorWidget(),
        }
        labels = {"content": "Содержание"}


class CustomSignupForm(SignupForm):
    def signup(self, request, user):
        user.save()


class RegisterUserForm(UserCreationForm):
    """Форма регистрации пользователя"""

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    email = forms.EmailField(max_length=200)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


class LoginUserForm(forms.Form):
    """Форма авторизации пользователя"""

    email = forms.EmailField(label="Почта")
    # username = forms.CharField(max_length=63)
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class UserPictureForm(forms.ModelForm):
    """Форма загрузки фотографий пользователя"""

    avatar_image = forms.ImageField(label="Profile Picture")
    hat_image = forms.ImageField(label="Hat Picture")

    class Meta:
        model = get_user_model()
        fields = (
            "avatar_image",
            "hat_image",
        )
