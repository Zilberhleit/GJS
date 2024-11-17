from django.shortcuts import render
from django.views.generic import ListView
from jam_polls.models import Question
from jams.models import GameJams


class PollList(ListView):
    model = Question
    template_name = 'pages/jam_polls_pages/poll.html'
    context_object_name = 'poll_list'

    def get_object(self, queryset=None):
        return GameJams.objects.get(uuid=self.kwargs.get('uuid'))


def submit_poll(request, uuid):
    if request.metchod == "POST":
        if "question_id" in request.HIDDEN:
            question_id = request.HIDDEN["question_id"]
