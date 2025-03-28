from django.contrib.auth import logout, login, authenticate
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView
from users.forms import LoginUserForm, RegisterUserForm
from users.models import User

from .services import get_user_past_jams_history


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'pages/user_pages/register.html'
    success_url = reverse_lazy('login')


def login_view(request):
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
    model = User
    template_name = 'pages/user_pages/user_profile.html'
    context_object_name = 'profile_data'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['past_jams'] = get_user_past_jams_history(self.request.user)

        return context


def logout_view(request):
    logout(request)
    return redirect('jams_list')


def avatar_view(request, username):
    if request.method == "POST":
        print('avafaf')
        if "photo" in request.FILES:
            avatar_photo = request.FILES["photo"]
            prev_avatar = User.objects.get(username=request.user.username)
            prev_avatar.avatar_image.update(avatar_photo)
            print("avafs", avatar_photo.file.name)

        return redirect('profile_detail', username=request.user.username)
    raise Http500


def redactor(request, username):
    return render(request, template_name='pages/user_pages/redaction_page.html')


def write_post():
    pass
