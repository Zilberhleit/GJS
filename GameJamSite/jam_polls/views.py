import json

from django.db.models import Value, IntegerField, F
from django.http import JsonResponse
from django.views.generic import ListView

from jam_polls.models import Question
from jams.models import GameJam


class PollList(ListView):
    model = Question
    template_name = 'pages/jam_polls_pages/poll.html'
    context_object_name = 'poll_list'

    def get_object(self, queryset=None):
        return GameJam.objects.get(uuid=self.kwargs.get('uuid'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["poll_jam_uuid"] = GameJam.objects.get(uuid=self.kwargs.get('uuid'))
        uuid = GameJam.objects.get(uuid=self.kwargs.get('uuid'))

        question_queryset = list(Question.objects.filter(jam_uuid=uuid).annotate(
            decision=Value(0, output_field=IntegerField())
        ).values('id', 'question_text', 'decision'))

        context["poll_list_json"] = question_queryset

        return context


def submit_poll(request, uuid):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for question in data['result']:

                question_id = question['id']
                answer = question['decision']
                current = Question.objects.filter(pk=question_id)

                if answer == 1:
                    current.update(count=F("count") + 1)
                elif answer == -1:
                    current.update(count=F("count") - 1)

                gamejam = GameJam.objects.get(uuid=uuid)
                gamejam.users.add(request.user)

            return JsonResponse({'message': 'Все вопросы пройдены', 'redirect': True})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)
