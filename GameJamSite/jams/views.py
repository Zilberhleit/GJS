from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render
import uuid


def jam_list_views(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/jams_pages/jams.html')


def jam_event_view(request: HttpRequest, jam_num: uuid) -> HttpResponse:
    return render(request, 'pages/jams_pages/event.html')


def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound(render(request, "pages/errors/404.html"))
