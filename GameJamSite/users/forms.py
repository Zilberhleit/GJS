from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms


class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

    email = forms.EmailField(max_length=200)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')




class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
