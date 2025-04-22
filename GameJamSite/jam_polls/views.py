import json
from uuid import UUID

from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views.generic import ListView

from jam_polls.models import ThemeVote, GameJamTheme
from jams.models import GameJam


class PollList(ListView):
    """ Представление списка вопросов для опроса """
    model = GameJamTheme
    template_name = 'pages/jam_polls_pages/poll.html'
    context_object_name = 'poll_list'

    def dispatch(self, request, *args, **kwargs):
        permission = check_user_vote_permission(request, self.kwargs.get('uuid'))
        return permission if permission else super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jam = GameJam.objects.get(uuid=self.kwargs.get('uuid'))
        context["poll_jam_uuid"] = jam

        question_queryset = GameJamTheme.objects.filter(gamejam=jam).values('id', 'theme')
        context["poll_list_json"] = list(question_queryset)

        return context


@transaction.atomic
def submit_poll(request, uuid: UUID):
    """ Представление для обработки ответов на опрос """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=403)
    if GameJam.objects.filter(uuid=uuid, users=request.user).exists():
        return JsonResponse({'error': 'Вы уже прошли опрос'}, status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for question in data['result']:
                question_id = question['id']
                answer = question['decision']

                ThemeVote.objects.create(
                    user=request.user,
                    theme=GameJamTheme.objects.get(pk=question_id),
                    vote=answer
                )

                gamejam = GameJam.objects.get(uuid=uuid)
                gamejam.users.add(request.user)

            return JsonResponse({'message': 'Все вопросы пройдены успешно', 'redirect': True})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)


def check_user_vote_permission(request, uuid: UUID):
    """  Проверка прав пользователя на прохождение опроса """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if GameJam.objects.filter(uuid=uuid, users=request.user).exists():
        return HttpResponseForbidden('Вы уже прошли опрос')
