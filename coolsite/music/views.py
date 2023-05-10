from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from .utils import *




class MusicHome(DataMixin, ListView):
    model = Album
    template_name = 'music/index.html'
    context_object_name = 'albums'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        c_def = self.get_user_context(title="Альбомы")
        return dict(list(context.items()) + list(c_def.items()))

def contact(request):
    return HttpResponseNotFound('Обратная связь')


class ShowAlbum(DataMixin, DetailView):
    model = Album
    template_name = 'music/album.html'
    slug_url_kwarg = 'album_slug'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracks'] = Track.objects.all()
        context['groups'] = Group.objects.all()
        c_def = self.get_user_context(title=context['album'])
        return dict(list(context.items()) + list(c_def.items()))


class MusicGroup(DataMixin, ListView):

    model = Group
    template_name = 'music/groups.html'
    context_object_name = 'groups'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Группы")
        return dict(list(context.items()) + list(c_def.items()))


class MusicTrack(DataMixin, ListView):

    model = Track
    template_name = 'music/tracks.html'
    context_object_name = 'tracks'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = Album.objects.all()
        context['groups'] = Group.objects.all()
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
        g = Genre.objects.get(slug=self.kwargs['genre_slug'])
        context['title'] = str(g.title)
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(3)
        context['menu'] = user_menu
        context['gen_selected'] = g.pk

        context['groups'] = Group.objects.all()
        context['albums'] = Album.objects.all()
        return context

    def get_queryset(self):
        return Track.objects.filter(genre__slug=self.kwargs['genre_slug'], is_published=True).select_related('genre')

class AddGroup(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddGroupForm
    template_name = 'music/addgroup.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление группы')
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'music/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'music/login.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')



