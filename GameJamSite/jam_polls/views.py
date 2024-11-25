import json
from django.http import JsonResponse, Http404
from django.shortcuts import redirect
from django.views.generic import ListView
from jam_polls.models import Question
from jams.models import GameJams


class PollList(ListView):
    model = Question
    template_name = 'pages/jam_polls_pages/poll.html'
    context_object_name = 'poll_list'

    def get_object(self, queryset=None):
        return GameJams.objects.get(uuid=self.kwargs.get('uuid'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["poll_jam_uuid"] = GameJams.objects.get(uuid=self.kwargs.get('uuid'))
        context["poll_list_json"] = json.dumps(list(self.get_queryset().values('id', 'question_text')))
        return context


def submit_poll(request, uuid):
    if request.method == "POST":
        if "question_id" in request.POST:
            question_id = int(request.POST.get('question_id'))
            answer = request.POST.get('answer')
            current_question = Question.objects.get(pk=question_id)

            if answer == '1':
                current_question.count += 1
            elif answer == '-1':
                if current_question.count > 0:
                    current_question.count -= 1

            current_question.save()

            next_question = Question.objects.filter(pk=question_id+1).first()
            if next_question:
                return JsonResponse({'question_id': next_question.id})
            else:
                if request.user.is_authenticated:
                    user = request.user
                    gamejam = GameJams.objects.get(uuid=uuid)
                    gamejam.users.add(user)
                    gamejam.save()
                    return JsonResponse({'message': 'Все вопросы пройдены', 'redirect': True})
                else:
                    return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=403)
