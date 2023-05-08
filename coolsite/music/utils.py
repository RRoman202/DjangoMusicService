
from .models import *

menu = [{'title': "Альбомы", 'url_name': 'home'},
        {'title': "Треки", 'url_name': 'tracks'},
        {'title': "Группы", 'url_name': 'groups'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Войти", 'url_name': 'login'}

]


class DataMixin:
        def get_user_context(self, **kwargs):
                context = kwargs
                genres = Genre.objects.all()
                groups = Group.objects.all()
                albums = Album.objects.all()
                tracks = Track.objects.all()
                context['menu'] = menu
                context['genres'] = genres
                context['albums'] = albums
                context['groups'] = groups
                context['tracks'] = tracks
                if 'gen_selected' not in context:
                        context['gen_selected'] = 0
                return context


