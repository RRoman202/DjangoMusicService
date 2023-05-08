from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import *
from .utils import *




class MusicHome(DataMixin, ListView):
    model = Album
    template_name = 'music/index.html'
    context_object_name = 'albums'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Альбомы")
        return dict(list(context.items()) + list(c_def.items()))

def about(request):
    return render(request, 'music/about.html', {'menu': menu, 'title': 'О сайте'})



def contact(request):
    return HttpResponseNotFound('Обратная связь')

def login(request):
    return HttpResponseNotFound('Авторизация')


class ShowAlbum(DataMixin, DetailView):
    model = Album
    template_name = 'music/album.html'
    slug_url_kwarg = 'album_slug'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['album'])
        return dict(list(context.items()) + list(c_def.items()))


def groups(request):
    groups = Group.objects.all()
    context = {
        'groups': groups,
        'menu': menu,
        'title': 'Группы'
    }
    return render(request, 'music/groups.html', context=context)

class MusicTrack(DataMixin, ListView):
    model = Track
    template_name = 'music/tracks.html'
    context_object_name = 'tracks'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Все треки')
        return dict(list(context.items()) + list(c_def.items()))


class ShowGroup(DataMixin, DetailView):
    model = Group
    template_name = 'music/group.html'
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['group'])
        return dict(list(context.items()) + list(c_def.items()))

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class MusicGenre(DataMixin, ListView):
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


