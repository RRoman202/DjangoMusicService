from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import *



menu = [{'title': "Альбомы", 'url_name': 'home'},
        {'title': "Треки", 'url_name': 'tracks'},
        {'title': "Группы", 'url_name': 'groups'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Войти", 'url_name': 'login'}

]

class MusicHome(ListView):
    model = Album
    template_name = 'music/index.html'
    context_object_name = 'albums'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['g_selected'] = 0
        context['groups'] = Group.objects.all()
        return context

def about(request):
    return render(request, 'music/about.html', {'menu': menu, 'title': 'О сайте'})



def contact(request):
    return HttpResponseNotFound('Обратная связь')

def login(request):
    return HttpResponseNotFound('Авторизация')


class ShowAlbum(DetailView):
    model = Album
    template_name = 'music/album.html'
    slug_url_kwarg = 'album_slug'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['album']
        context['menu'] = menu
        return context


# def show_album(request, album_slug):
#     album = get_object_or_404(Album, slug=album_slug)
#
#     context = {
#         'album': album,
#         'menu': menu,
#         'title': album.title,
#         'g_selected': album.group_id
#     }
#     return render(request, 'music/album.html', context=context)

def groups(request):
    groups = Group.objects.all()
    context = {
        'groups': groups,
        'menu': menu,
        'title': 'Группы'
    }
    return render(request, 'music/groups.html', context=context)

class MusicTrack(ListView):
    model = Track
    template_name = 'music/tracks.html'
    context_object_name = 'tracks'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все треки'
        context['menu'] = menu
        context['gen_selected'] = 0
        context['groups'] = Group.objects.all()
        context['albums'] = Album.objects.all()
        return context


def show_group(request, group_id):
    return HttpResponse(f'Отображение группы с id = {group_id}')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class MusicGenre(ListView):
    model = Track
    template_name = 'music/tracks.html'
    context_object_name = 'tracks'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['tracks'][0].genre)
        context['menu'] = menu
        context['gen_selected'] = context['tracks'][0].genre_id
        context['groups'] = Group.objects.all()
        context['albums'] = Album.objects.all()
        return context

    def get_queryset(self):
        return Track.objects.filter(genre__slug=self.kwargs['genre_slug'], is_published=True)


