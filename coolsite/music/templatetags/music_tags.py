import requests
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
@register.simple_tag(name='getphoto')
def get_photo(urltext):
    if 'https' in urltext:
        return 'htp'
    else:
        return 'no'
@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

