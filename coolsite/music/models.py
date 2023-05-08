from django.db import models
from django.urls import reverse
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
        ordering = ['time_create', 'title']

    def get_absolute_url(self):
        return reverse('album', kwargs={'album_slug': self.slug})

class Group(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    date_create = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('group', kwargs={'group_slug': self.slug})

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