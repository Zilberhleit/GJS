from django.shortcuts import render
from django.views.generic import ListView
from jam_polls.models import Question


class PollList(ListView):
    pass
