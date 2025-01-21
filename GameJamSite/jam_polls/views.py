import json
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, render
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
        uuid = GameJams.objects.get(uuid=self.kwargs.get('uuid'))
        question_dict = []
        for question in Question.objects.filter(jam_uuid=uuid):
            question_dict.append({
                'id': question.pk,
                'text': question.question_text,
                'decision': 0})
        context["poll_list_json"] = json.dumps(question_dict)
        return context


def submit_poll(request, uuid):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for question in data['result']:
                question_id = question['id']
                answer = question['decision']
                current = Question.objects.get(pk=int(question_id))
                if answer == 1:
                    current.count += 1
                elif answer == -1:
                    if current.count > 0:
                        current.count -= 1

                if request.user.is_authenticated:
                    current.save()
                    user = request.user
                    gamejam = GameJams.objects.get(uuid=uuid)
                    gamejam.users.add(user)
                    gamejam.save()
                    return JsonResponse({'message': 'Все вопросы пройдены', 'redirect': True})
                else:
                    return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=403)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)
        # if "question_id" in request.POST:
        #     question_id = int(request.POST.get('question_id'))
        #     answer = request.POST.get('answer')
        #     print('q_id', question_id)
        #     print('ans', answer)
        #     current_question = Question.objects.get(pk=question_id)
        #     print('q_text', current_question.question_text)
        #
        #     if answer == '1':
        #         current_question.count += 1
        #     elif answer == '-1':
        #         if current_question.count > 0:
        #             current_question.count -= 1
        #
        #     current_question.save()
        #
        #     next_question = Question.objects.filter(pk=question_id+1).first()
        #     print('nq_text', next_question.question_text)
        #     if next_question:
        #         return JsonResponse({'question_id': next_question.id})
        #     else:
        #         if request.user.is_authenticated:
        #             user = request.user
        #             gamejam = GameJams.objects.get(uuid=uuid)
        #             gamejam.users.add(user)
        #             gamejam.save()
        #             return JsonResponse({'message': 'Все вопросы пройдены', 'redirect': True})
        #         else:
        #             return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=403)
