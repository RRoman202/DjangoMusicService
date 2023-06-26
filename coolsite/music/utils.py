from django.db.models import Count

from .models import *
import json
from typing import List, Tuple, Optional
import re
from bs4 import BeautifulSoup as bs


import dpath.util

import requests

menu = [{'title': "Альбомы", 'url_name': 'home'},
        {'title': "Треки", 'url_name': 'tracks'},
        {'title': "Исполнители", 'url_name': 'groups'},
        {'title': "Рекомендации", 'url_name': 'recs'},
        {'title': "Предсказание", 'url_name': 'pred'},


]


class DataMixin:
        paginate_by = 5
        def get_user_context(self, **kwargs):
                context = kwargs
                genres = Genre.objects.all()
                user_menu = menu.copy()
                context['menu'] = user_menu
                context['genres'] = genres
                if 'gen_selected' not in context:
                        context['gen_selected'] = 0
                return context


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'


PATTERNS = [
    re.compile(r'window\["ytInitialData"\] = (\{.+?\});'),
    re.compile(r'var ytInitialData = (\{.+?\});'),
]

session = requests.Session()
session.headers['User-Agent'] = USER_AGENT

#метод получения данных результата поиска видео
def get_ytInitialData(url: str) -> Optional[dict]:
    rs = session.get(url)

    for pattern in PATTERNS:
        m = pattern.search(rs.text)
        if m:
            data_str = m.group(1)
            return json.loads(data_str)


#метод получения ссылок и загловков видео
def search_youtube(group, text_or_url: str) -> List[Tuple[str, str]]:
    if text_or_url.startswith('http'):
        url = text_or_url
    else:
        text = text_or_url
        url = f'https://www.youtube.com/results?search_query={text}'

    items = []

    data = get_ytInitialData(url)


    if not data:
        return items

    videos = dpath.util.values(data, '**/videoRenderer')
    if not videos:
        videos = dpath.util.values(data, '**/playlistVideoRenderer')

    print(len(videos))
    for video in videos:
        if 'videoId' not in video:
            continue

        url = 'https://www.youtube.com/watch?v=' + video['videoId']
        try:
            title = dpath.util.get(video, 'title/runs/0/text')
        except KeyError:
            title = dpath.util.get(video, 'title/simpleText')

        items.append((url, title))
        break

    return items[0][0]



