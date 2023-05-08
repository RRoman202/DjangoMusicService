from django import template
from music.models import *

register = template.Library()

@register.simple_tag(name='getgen')
def get_genres():
    return Genre.objects.all()

@register.inclusion_tag('music/list_genres.html')
def show_genres(sort=None, gen_selected=0):
    if not sort:
        genres = Genre.objects.all()
    else:
        genres = Genre.objects.order_by(sort)
    return {"genres": genres, 'gen_selected': gen_selected}

@register.simple_tag(name='getal')
def get_albums():
    return Album.objects.all()

