from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', MusicHome.as_view(), name='home'),
    path('addgroup/', AddGroup.as_view(), name='addgroup'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('addalbumuser', add_album_user, name='addalbum'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('album/<slug:album_slug>/', ShowAlbum.as_view(), name='album'),
    path('groups/', MusicGroup.as_view(), name='groups'),
    path('groups/group/<slug:group_slug>/', ShowGroup.as_view(), name='group'),
    path('tracks/', MusicTrack.as_view(), name='tracks'),
    path('genre/<slug:genre_slug>/', MusicGenre.as_view(), name='genre'),
    path('recs/', MusicRecomendationAlbum.as_view(), name='recs'),
    path('pred/', upload_file, name='pred'),
    path('predresult/', PredResult.as_view(), name='predresult'),
    path('track/<slug:track_slug>/', ShowTrack.as_view(), name='track'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('searchtracks/', SearchResultsTrackView.as_view(), name='search_results_tracks'),
    path('profile/', ProfileView.as_view(), name='prof'),
]