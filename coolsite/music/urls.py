from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', MusicHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('album/<slug:album_slug>/', ShowAlbum.as_view(), name='album'),
    path('groups/', groups, name='groups'),
    path('groups/group/<int:group_id>/', show_group, name='group'),
    path('tracks/', MusicTrack.as_view(), name='tracks'),
    path('genre/<slug:genre_slug>/', MusicGenre.as_view(), name='genre'),

]