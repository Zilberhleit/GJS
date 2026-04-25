from enum import member
from tempfile import template

from allauth.account import app_settings
from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.generic import CreateView, DetailView
from jams.models.gamejam import GameJam
from jams.models.rating_user_jam import RatingCriterion

from users.forms import LoginUserForm, RegisterUserForm
from users.models import Follower, Notification, Team, TeamInvitation, User
from users.models.team import TeamMembership
from users.utils import send_realtime_notification

from .services import (
    get_user_created_teams,
    get_user_followers,
    get_user_games_history,
    get_user_jams_history,
    is_valid_create_team,
    is_valid_criterion,
    is_valid_gamejam_create,
    upload_photo,
)


class RegisterUser(CreateView):
    """Представление регистрации пользователя"""

    form_class = RegisterUserForm
    template_name = "pages/user_pages/register.html"
    success_url = reverse_lazy("login")


def login_view(request):
    """Представление входа в аккаунт"""
    if request.method == "POST":
        form = LoginUserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(
                    reverse(
                        "profile_detail",
                        kwargs={
                            "username": user.username,
                            # 'upload_data':upload_data
                        },
                    )
                )
            else:
                form.add_error(None, "Неверный адрес электронной почты или пароль.")
    else:
        form = LoginUserForm()
    return render(request, "pages/user_pages/login.html", context={"form": form})


class Profile(DetailView):
    """Представление профиля пользователя"""

    model = User
    template_name = "pages/user_pages/user_profile.html"
    context_object_name = "profile_data"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["past_jams"] = get_user_jams_history(self.kwargs.get("username"))
        context["user_games"] = get_user_games_history(self.kwargs.get("username"))
        context["upload_data"] = {
            "upload_url": reverse("upload-photo", args=[self.kwargs.get("username")])
        }
        # new context
        context["created_teams"] = get_user_created_teams(self.kwargs.get("username"))
        context["first_created_team"] = get_user_created_teams(
            self.kwargs.get("username")
        ).first()
        context["subscribers"] = get_user_followers(self.kwargs.get("username"))
        context["subscribers_count"] = get_user_followers(
            self.kwargs.get("username")
        ).count()
        context["follow_data"] = {
            "follow_url": reverse("follow", args=[self.kwargs.get("username")]),
            "unfollow_url": reverse("unfollow", args=[self.kwargs.get("username")]),
        }
        return context


def logout_view(request):
    """Представление выхода из аккаунта"""
    logout(request)
    return redirect("home_page")


def upload_photo_view(request, username):
    """Представление загрузки фото (аватара или шапки)"""

    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        if "avatar_image" in request.FILES:
            if upload_photo("avatar_image", request.FILES, user):
                return JsonResponse(
                    {
                        "message": "Фото успешно загружено",
                        "avatar": user.avatar_image.url,
                    }
                )

        elif "hat_image" in request.FILES:
            if upload_photo("hat_image", request.FILES, user):
                return JsonResponse(
                    {"message": "Шапка успешно загружена", "hat": user.hat_image.url}
                )

        else:
            return JsonResponse(
                {
                    "message": "Предоставлен неверный формат файла / Размер файла превышает 3Мб"
                }
            )


@login_required
def about_page(request):
    return render(request, "pages/about.html")


@login_required
def follow(request, username):
    """Представление подписки на пользователя"""
    try:
        following_user = get_object_or_404(User, username=username)

        if request.user == following_user:
            return JsonResponse(
                {"status": "error", "message": "Нельзя подписаться на себя"}
            )

        Follower.objects.get_or_create(follower=request.user, following=following_user)
        return JsonResponse(
            {"status": "ok", "message": f"Вы подписались на {following_user.username}"}
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def unfollow(request, username):
    """Представление отписки на пользователя"""
    try:
        following_user = get_object_or_404(User, username=username)
        deleted, _ = Follower.objects.filter(
            follower=request.user, following=following_user
        ).delete()

        if deleted == 0:
            JsonResponse({"status": "error", "message": "Вы не были подписаны"})

        return JsonResponse(
            {"status": "ok", "message": f"Вы отписались на {following_user.username}"}
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def create_jam(request):
    """Представление создание джема"""
    if request.method == "POST":
        title = request.POST.get("title", "")
        theme = request.POST.get("theme", "")
        description = request.POST.get("description", "")
        date_start_str = request.POST.get("date_start")
        date_end_str = request.POST.get("date_end")
        date_rating_str = request.POST.get("date_rating")

        date_start = parse_datetime(date_start_str)
        date_end = parse_datetime(date_end_str)
        date_rating = parse_datetime(date_rating_str)

        if date_start:
            date_start = timezone.make_aware(date_start)
        if date_end:
            date_end = timezone.make_aware(date_end)
        if date_rating:
            date_rating = timezone.make_aware(date_rating)

        is_valid = is_valid_gamejam_create(
            title, theme, date_start, date_end, date_rating
        )

        if not is_valid:
            return render(request, template_name="pages/user_pages/create_jam.html")
        else:
            jam = GameJam.objects.create(
                author=request.user,
                title=title.strip(),
                theme=theme.strip(),
                description=description.strip() if description else "",
                date_start=date_start,
                date_end=date_end,
                date_rating=date_rating,
            )
            create_critreria(request, jam)
            return redirect("gamejam_detail", uuid=jam.uuid)
    return render(request, template_name="pages/user_pages/create_jam.html")


def create_critreria(request, jam):
    """Создание критериев оценки"""
    for key, value in request.POST.items():
        if key.startswith("field"):
            if is_valid_criterion(value):
                try:
                    RatingCriterion.objects.create(
                        name=value.strip(),
                        jam=jam,
                    )
                except Exception as e:
                    print(f"Error in saving at {key}: {e}")


@login_required
def create_team(request):
    """Представление создания команды"""
    if request.method == "POST":
        if Team.objects.filter(created_by=request.user).exists():
            return redirect("profile_detail", username=request.user.username)

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        leader = request.user

        is_valid = is_valid_create_team(title)

        if is_valid:
            team = Team.objects.create(
                name=title, description=description, created_by=leader
            )

            TeamMembership.objects.create(team=team, user=leader, role="leader")
            return redirect("profile_detail", username=request.user.username)
    return render(request, template_name="pages/user_pages/create_team.html")


def team_detail(request, id):
    team = get_object_or_404(Team, id=id)
    is_leader = False
    if request.user.is_authenticated:
        membership = team.teammembership_set.filter(user=request.user).first()
        is_leader = membership and membership.role == "leader"

    return render(
        request,
        template_name="pages/user_pages/team_detail.html",
        context={
            "team": team,
            "is_leader": is_leader,
        },
    )


@login_required
def notifications(request):
    return render(request, template_name="pages/user_pages/notification.html")


@login_required
def invite_to_team(request, id):
    team = get_object_or_404(Team, id=id)

    is_leader = TeamMembership.objects.filter(
        team=team, user=request.user, role="leader"
    ).exists()

    if not is_leader:
        messages.error(request, "Только лидер может приглашать")
        return redirect("team_detail", id=team.id)

    if request.method == "POST":
        username = request.POST.get("username")
        invited_user = get_object_or_404(User, username=username)

        if invited_user == request.user:
            messages.error(request, "Нельзя пригласить себя")
            return redirect("team_detail", id=team.id)

        if team.members.filter(id=invited_user.id).exists():
            messages.error(request, "Пользователь уже в команде")
            return redirect("team_detail", id=team.id)

        message = f"Пользователь {request.user} приглашает вас в команду {team.name}"

        invitation = TeamInvitation.objects.create(
            team=team, invitee=invited_user, inviter=request.user, status="pending"
        )

        notification = Notification.objects.create(
            recipient=invited_user,
            sender=request.user,
            notification_type="team_invite",
            team=team,
            message=message,
        )

        send_realtime_notification(
            user_id=invited_user.id,
            message=message,
            notification_id=notification.id,
            notification_type="info",
        )
        return redirect("team_detail", id=team.id)
    return render(request, "users/invite_to_team.html", {"team": team})


@login_required
def accept_invite(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    invitation = get_object_or_404(
        TeamInvitation, team=team, invitee=request.user, status="pending"
    )
    invitation.status = "accepted"
    invitation.save()

    TeamMembership.objects.get_or_create(
        team=team, user=request.user, defaults={"role": "member"}
    )

    message = f"Пользователь {request.user.username} теперь в вашей команде"

    notification = Notification.objects.create(
        recipient=invitation.inviter,
        sender=request.user,
        notification_type="team_accept",
        team=team,
        message=message,
    )

    send_realtime_notification(
        user_id=invitation.inviter.id,
        message=message,
        notification_id=notification.id,
        notification_type="info",
    )

    return JsonResponse({"status": "ok"})


@login_required
def reject_invite(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    invitation = get_object_or_404(
        TeamInvitation, team=team, invitee=request.user, status="pending"
    )
    invitation.status = "reject"
    invitation.save()

    message = f"Пользователь {request.user.username} теперь в вашей команде"

    notification = Notification.objects.create(
        recipient=invitation.inviter,
        sender=request.user,
        notification_type="team_accept",
        team=team,
        message=message,
    )

    send_realtime_notification(
        user_id=invitation.inviter.id,
        message=message,
        notification_id=notification.id,
        notification_type="info",
    )

    return JsonResponse({"status": "ok"})


@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by(
        "-created_at"
    )[:50]
    data = []
    for n in notifications:
        item = {
            "id": n.id,
            "message": n.message,
            "created_at": n.created_at.isoformat(),
            "type": n.notification_type,
            "is_read": n.is_read,
        }
        if n.notification_type == "team_invite":
            item["team_id"] = n.team.id

        data.append(item)
    return JsonResponse(
        {
            "notifications": data,
            "unread_count": sum(1 for n in notifications if not n.is_read),
        }
    )


@login_required
def notification_read(request, notification_id):
    notification = get_object_or_404(
        Notification, id=notification_id, recipient=request.user
    )
    notification.is_read = True
    notification.save()
    return JsonResponse({"status": "ok"})


def search_users(request):
    query = request.GET.get("q", "")
    if len(query) < 2:
        return JsonResponse([], safe=False)

    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)[
        :10
    ]

    data = [{"username": user.username} for user in users]
    return JsonResponse(data, safe=False)


def redactor(request, username):
    """Представление редактирования страницы пользователя"""
    return render(request, template_name="pages/user_pages/redaction_page.html")


def write_post():
    """Представление создания поста"""
    pass
