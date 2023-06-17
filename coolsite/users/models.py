
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
import music.models


class CustomUser(AbstractUser):
    albums_list = models.ManyToManyField(music.models.Album)
    groups_list = models.ManyToManyField(music.models.Group)
    tracks_list = models.ManyToManyField(music.models.Track)
