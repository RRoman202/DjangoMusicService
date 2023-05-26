from django.contrib import admin
from embed_video.admin import AdminVideoMixin


from .models import *


class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class TrackAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}

class MusicVideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(MusicVideo, MusicVideoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Genre, GenreAdmin)
