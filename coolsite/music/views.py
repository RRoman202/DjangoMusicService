from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *



menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

def index(request):
    albums = Album.objects.all()
    groups = Group.objects.all()
    context = {
        'albums': albums,
        'groups': groups,
        'menu': menu,
        'title': 'Главная страница',
        'g_selected': 0
    }
    return render(request, 'music/index.html', context=context)

def about(request):
    return render(request, 'music/about.html', {'menu': menu, 'title': 'О сайте'})



def contact(request):
    return HttpResponseNotFound('Обратная связь')

def login(request):
    return HttpResponseNotFound('Авторизация')

def show_album(request, album_id):
    return HttpResponse(f'Отображение альбома с id = {album_id}')

def groups(request):
    groups = Group.objects.all()
    context = {
        'groups': groups,
        'menu': menu,
        'title': 'Группы'
    }
    return render(request, 'music/groups.html', context=context)

def show_group(request, group_id):
    return HttpResponse(f'Отображение группы с id = {group_id}')



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
