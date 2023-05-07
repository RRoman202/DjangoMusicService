from django.db import models
from django.urls import reverse
# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    year = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('album', kwargs={'album_id': self.pk})

class Group(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    date_create = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url_groups(self):
        return reverse('group', kwargs={'group_id': self.pk})
