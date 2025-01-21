from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import LoginUserForm, RegisterUserForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import logout
from users.models import User


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'pages/user_pages/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    template_name = 'pages/user_pages/login.html'
    form_class = LoginUserForm

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('profile_detail', kwargs={'username': user.username})


class Profile(DetailView):
    model = User
    template_name = 'pages/user_pages/user_profile.html'
    context_object_name = 'profile_data'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)


def logout_view(request):
    logout(request)
    return redirect('jams_list')


def redactor(request, username):
    return render(request, template_name='pages/user_pages/redaction_page.html')


def write_post():
    return None