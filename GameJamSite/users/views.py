from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import LoginUserForm, RegisterUserForm
from django.views.generic import ListView, DetailView


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'pages/user_pages/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    template_name = 'pages/user_pages/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('homepage')


class Profile(DetailView):
    pass


class GameList(ListView):
    pass