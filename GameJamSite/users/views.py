from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView

from users.forms import LoginUserForm, RegisterUserForm
from users.models import User
from .services import get_user_jams_history, get_user_games_history, upload_photo


class RegisterUser(CreateView):
    """  Представление регистрации пользователя """
    form_class = RegisterUserForm
    template_name = 'pages/user_pages/register.html'
    success_url = reverse_lazy('login')


def login_view(request):
    """  Представление входа в аккаунт """
    if request.method == "POST":
        form = LoginUserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('profile_detail', kwargs={'username': user.username}))
            else:
                form.add_error(None, 'Неверный адрес электронной почты или пароль.')
    else:
        form = LoginUserForm()
    return render(request, 'pages/user_pages/login.html', context={'form': form})


class Profile(DetailView):
    """ Представление профиля пользователя """

    model = User
    template_name = 'pages/user_pages/user_profile.html'
    context_object_name = 'profile_data'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['past_jams'] = get_user_jams_history(self.kwargs.get('username'))
        context['user_games'] = get_user_games_history(self.kwargs.get('username'))
        return context


def logout_view(request):
    """  Представление выхода из аккаунта """
    logout(request)
    return redirect('jams_list')


def upload_photo_view(request, username):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        if "avatar_image" in request.FILES:
            if upload_photo("avatar_image", request.FILES, user):
                return JsonResponse({'message': 'Фото успешно загружено', 'avatar': user.avatar_image.url})

        elif "hat_image" in request.FILES:
            if upload_photo("hat_image", request.FILES, user):
                return JsonResponse({'message': 'Шапка успешно загружена', 'hat': user.hat_image.url})

        else:
            return JsonResponse({'message': 'Предоставлен неверный формат файла / Размер файла превышает 3Мб'})


def redactor(request, username):
    """  Представление редактирования страницы пользователя """
    return render(request, template_name='pages/user_pages/redaction_page.html')


def write_post():
    """  Представление создания поста """
    pass
