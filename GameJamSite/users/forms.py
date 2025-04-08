from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    """ Форма регистрации пользователя   """

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

    email = forms.EmailField(max_length=200)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(forms.Form):
    """  Форма авторизации пользователя   """
    email = forms.EmailField(label='Почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class UserPictureForm(forms.ModelForm):
    """  Форма загрузки фотографий пользователя   """
    avatar_image = forms.ImageField(label="Profile Picture")
    hat_image = forms.ImageField(label="Hat Picture")

    class Meta:
        model = get_user_model()
        fields = ("avatar_image", "hat_image",)
