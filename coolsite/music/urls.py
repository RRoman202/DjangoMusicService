from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('album/<int:album_id>/', show_album, name='album'),
    path('groups/', groups, name='groups'),
    path('groups/group/<int:group_id>/', show_group, name='group')

]