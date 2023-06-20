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
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

