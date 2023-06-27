import textwrap

from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Max
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.core.cache import cache
from hitcount.views import HitCountDetailView
from hitcount.models import *
import io
from reportlab.pdfgen import canvas
from django.http import FileResponse
from .forms import *
from .models import *
from .utils import *
from django.db.models import Q
import joblib
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.http import JsonResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def pdfview(request, id_album):
    pdfmetrics.registerFont(TTFont('Tahoma', 'Tahoma.ttf'))

    album = Album.objects.get(id=id_album)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Tahoma", 14)
    text = album.description
    text = textwrap.wrap(text, width=50)
    lines = [
        album.title,
        str(album.year),



    ]
    for t in text:
        lines.append(t)
    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='pdf_album.pdf')


def pdfview_group(request, id_group):
    pdfmetrics.registerFont(TTFont('Tahoma', 'Tahoma.ttf'))

    album = Group.objects.get(id=id_group)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Tahoma", 14)
    text = album.description
    text = textwrap.wrap(text, width=50)
    lines = [
        album.title,
    ]
    for t in text:
        lines.append(t)
    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='pdf_group.pdf')

class MusicHome(DataMixin, ListView):

    model = Album
    template_name = 'music/index.html'
    context_object_name = 'albums'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()

        c_def = self.get_user_context(title="Альбомы")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            object_list = Album.objects.filter(
                Q(title__iregex=query) | Q(group__title__iregex=query)
            )
            return object_list
        else:
            object_list = Album.objects.all()

            return object_list

class PlaylistView(DataMixin, ListView):
    paginate_by = 10
    model = Playlist
    template_name = 'music/playlists.html'
    context_object_name = 'playlists'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)


        c_def = self.get_user_context(title="Мои плейлисты")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            object_list = Playlist.objects.filter(
                Q(title__iregex=query)
            )
            return object_list
        else:
            object_list = Playlist.objects.all()

            return object_list

class ProfileView(LoginRequiredMixin, DataMixin, TemplateView):

    template_name = 'music/profile.html'



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()

        c_def = self.get_user_context(title="Профиль")
        return dict(list(context.items()) + list(c_def.items()))




class MusicRecomendationAlbum(DataMixin, TemplateView):


    model = Album
    template_name = 'music/recomendation.html'
    context_object_name = 'albums'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['hits'] = HitCount.objects.order_by('-hits')[0:3]
        context['albums'] = Album.objects.all()
        c_def = self.get_user_context(title="Популярные альбомы")
        return dict(list(context.items()) + list(c_def.items()))




class ShowAlbum(DataMixin, HitCountDetailView):
    model = Album
    template_name = 'music/album.html'
    slug_url_kwarg = 'album_slug'
    count_hit = True
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracks'] = Track.objects.all()
        context['groups'] = Group.objects.all()
        context['vid'] = search_youtube(context['album'].group.title, 'intitle:' + ''.join(context['album'].group.title) + '-' + ''.join(context['album'].title))
        context['count_tracks'] = Track.objects.all().filter(album=context['album']).count()
        c_def = self.get_user_context(title=context['album'])
        return dict(list(context.items()) + list(c_def.items()))

class ShowTrack(DataMixin, DetailView):
    model = Track
    template_name = 'music/track.html'
    slug_url_kwarg = 'track_slug'
    count_hit = True
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vid'] = search_youtube(context['track'].album.group.title, 'intitle:' + ''.join(context['track'].album.group.title) + '-' + ''.join(context['track'].title))
        context['recs'] = Track.objects.order_by('?').filter(genre=context['track'].genre)[0:3]
        c_def = self.get_user_context(title=context['track'])
        return dict(list(context.items()) + list(c_def.items()))


class MusicGroup(DataMixin, ListView):
    paginate_by = 10
    model = Group
    template_name = 'music/groups.html'
    context_object_name = 'groups'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_url'] = False
        c_def = self.get_user_context(title="Исполнители")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):

        query = self.request.GET.get('q', None)
        if query:
            object_list = Group.objects.order_by('id').filter(
                Q(title__iregex=query)
            )
            return object_list
        else:
            object_list = Group.objects.order_by('id')

            return object_list
        return Group.objects.order_by('id')


class MusicTrack(DataMixin, ListView):

    paginate_by = 10
    model = Track
    template_name = 'music/tracks.html'
    context_object_name = 'tracks'
    allow_empty = True


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = Album.objects.all()
        context['groups'] = Group.objects.all()

        c_def = self.get_user_context(title='Все треки')

        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):

        return redirect('home')
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            object_list = Track.objects.filter(
                Q(title__iregex=query) | Q(album__title__iregex=query) | Q(album__group__title__iregex=query)
            )
            return object_list
        else:
            object_list = Track.objects.all()

            return object_list
class MusicTrackPlaylist(DataMixin, ListView):


    paginate_by = 10
    model = Track
    template_name = 'music/addtracksinplaylist.html'
    context_object_name = 'tracks'
    allow_empty = True


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = Album.objects.all()
        context['groups'] = Group.objects.all()
        context['playlist_id'] = cache.get('playlist_id')
        context['playlist'] = Playlist.objects.get(id=cache.get('playlist_id'))

        c_def = self.get_user_context(title='Добавление треков')

        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):

        return redirect('home')
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            object_list = Track.objects.filter(
                Q(title__iregex=query) | Q(album__title__iregex=query) | Q(album__group__title__iregex=query)
            )
            return object_list
        else:
            object_list = Track.objects.all()

            return object_list


class ShowGroup(DataMixin, HitCountDetailView):
    model = Group
    template_name = 'music/group.html'
    slug_url_kwarg = 'group_slug'
    count_hit = True
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = Album.objects.all()
        c_def = self.get_user_context(title=context['group'])
        return dict(list(context.items()) + list(c_def.items()))

class ShowPlaylist(DataMixin, HitCountDetailView):
    model = Playlist
    template_name = 'music/playlist.html'

    count_hit = True
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cache.set('playlist_id', context['playlist'].id)
        context['albums'] = Album.objects.all()
        context['groups'] = Group.objects.all()
        c_def = self.get_user_context(title=context['playlist'])
        return dict(list(context.items()) + list(c_def.items()))

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class MusicGenre(DataMixin, ListView):

    model = Track
    template_name = 'music/tracks.html'
    context_object_name = 'tracks'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g = Genre.objects.get(slug=self.kwargs['genre_slug'])
        context['title'] = str(g.title)
        user_menu = menu.copy()

        context['menu'] = user_menu
        context['gen_selected'] = g.pk

        context['groups'] = Group.objects.all()
        context['albums'] = Album.objects.all()
        return context


    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            object_list = Track.objects.filter(
                Q(title__iregex=query) | Q(album__title__iregex=query) | Q(album__group__title__iregex=query)
            )
            return object_list.filter(genre__slug=self.kwargs['genre_slug'], is_published=True).select_related('genre')
        else:
            object_list = Track.objects.all()

            return object_list.filter(genre__slug=self.kwargs['genre_slug'], is_published=True).select_related('genre')




class AddPlaylist(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPlaylistForm
    template_name = 'music/addplaylist.html'
    success_url = reverse_lazy('prof')
    login_url = reverse_lazy('prof')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание плейлиста')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

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

def add_track_playlist(request, id_playlist, id_track):
    playlist = Playlist.objects.get(id=id_playlist)
    track = Track.objects.get(id=id_track)
    playlist.tracks_list.add(track)

    return redirect(request.META.get('HTTP_REFERER'))


def delete_track_playlist(request, id_playlist, id_track):
    playlist = Playlist.objects.get(id=id_playlist)
    track = Track.objects.get(id=id_track)
    playlist.tracks_list.remove(track)

    return redirect(request.META.get('HTTP_REFERER'))

def delete_playlist(request, id_playlist):
    Playlist.objects.get(id=id_playlist).delete()

    return redirect(request.META.get('HTTP_REFERER'))

def add_album_user(request, id):
    album = Album.objects.get(id=id)
    request.user.albums_list.add(album)
    return redirect(request.META.get('HTTP_REFERER'))

def delete_album_user(request, id):
    album = Album.objects.get(id=id)
    request.user.albums_list.remove(album)
    return redirect(request.META.get('HTTP_REFERER'))

def add_group_user(request, id):
    group = Group.objects.get(id=id)
    request.user.groups_list.add(group)
    return redirect(request.META.get('HTTP_REFERER'))

def delete_group_user(request, id):
    group = Group.objects.get(id=id)
    request.user.groups_list.remove(group)
    return redirect(request.META.get('HTTP_REFERER'))

def add_track_user(request, id):
    track = Track.objects.get(id=id)
    request.user.tracks_list.add(track)
    return redirect(request.META.get('HTTP_REFERER'))

def delete_track_user(request, id):
    track = Track.objects.get(id=id)
    request.user.tracks_list.remove(track)
    return redirect(request.META.get('HTTP_REFERER'))

def handle_uploaded_file(f):
    model = joblib.load('music/model.pkl')

    output = " "
    for chunk in f.chunks():
        output += chunk.decode('utf-8')
    output = output.replace("\n", "").replace("\r", "")
    print(model.predict([output]))
    return model.predict([output])

def upload_file(request):
    user_menu = menu.copy()

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            genre_pred = handle_uploaded_file(request.FILES["file"])
            genre_pred = genre_pred[0]
            cache.set('genre_pred', genre_pred)
            return redirect('predresult')
    else:
        form = UploadFileForm()
    return render(request, "music/pred.html", {"form": form, "menu": user_menu})

class PredResult(DataMixin, TemplateView):
    template_name = "music/predresult.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PredResult, self).get_context_data(*args, **kwargs)
        c_def = self.get_user_context(title='Результат')

        context['genre_pred'] = cache.get('genre_pred')
        cache.delete('genre_pred')
        return dict(list(context.items()) + list(c_def.items()))



