
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
import music.models


class CustomUser(AbstractUser):
    albums_list = models.ManyToManyField(music.models.Album)
    groups_list = models.ManyToManyField(music.models.Group)
    tracks_list = models.ManyToManyField(music.models.Track)
    playlists_list = models.ManyToManyField(music.models.Playlist)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", default=0)
