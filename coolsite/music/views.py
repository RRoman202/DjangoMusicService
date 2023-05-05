from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render

def index(request):
    return HttpResponse("Страница приложения music")

def genres(request, genid):
    if(request.GET):
        print(request.GET)
    return HttpResponse(f"<h1>Музыка по жанрам</h1><p>{genid}</p>")

def archive(request, year):
    if(int(year) > 2023):
        raise Http404()
    return HttpResponse(f"<h1>Музыка по годам</h1><p>{year}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
