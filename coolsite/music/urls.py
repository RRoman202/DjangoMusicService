from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index),
    path('genres/<int:genid>/', genres),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive)
]