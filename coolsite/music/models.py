from django.db import models
from django.urls import reverse
from embed_video.fields import EmbedVideoField
# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    year = models.IntegerField(default=0)
    group = models.ForeignKey('Group', on_delete=models.PROTECT)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Альбомы'
        verbose_name_plural = 'Альбомы'
        ordering = ['-time_create', 'title']

    def get_absolute_url(self):
        return reverse('album', kwargs={'album_slug': self.slug})

    def album_as_list(self):
        return self.photo.url.split('/')

class Group(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name="Название группы")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    date_create = models.CharField(max_length=255, verbose_name="Год основания")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('group', kwargs={'group_slug': self.slug})

    class Meta:
        verbose_name = 'Группы'
        verbose_name_plural = 'Группы'
        ordering = ['-time_create', 'title']

    def group_as_list(self):
        return self.photo.url.split('/')

class Track(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    album = models.ForeignKey('Album', on_delete=models.PROTECT)
    genre = models.ForeignKey('Genre', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Треки'
        verbose_name_plural = 'Треки'
        ordering = ['-time_create', 'title']

    def get_absolute_url(self):
        return reverse('track', kwargs={'track_slug': self.slug})

class Genre(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})


class Playlist(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    tracks_list = models.ManyToManyField(Track)
    user_id = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('playlist', kwargs={'playlist_slug': self.slug})



class MusicVideo(models.Model):
    title = models.CharField(max_length=255)
    music_Video = EmbedVideoField()

    class Meta:
        verbose_name_plural = "Видео"

