from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

def jam_list_views(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/jams_pages/jams.html')

def jam_load(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Load your game")