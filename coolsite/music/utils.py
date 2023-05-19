from django.db.models import Count

from .models import *

menu = [{'title': "Альбомы", 'url_name': 'home'},
        {'title': "Треки", 'url_name': 'tracks'},
        {'title': "Группы", 'url_name': 'groups'},
        {'title': "Рекомендации", 'url_name': 'recs'},
        {'title': "Предсказание", 'url_name': 'pred'},
        {'title': "Добавить группу", 'url_name': 'addgroup'},

]


class DataMixin:
        paginate_by = 5
        def get_user_context(self, **kwargs):
                context = kwargs
                genres = Genre.objects.all()
                user_menu = menu.copy()
                if not self.request.user.is_authenticated:
                        user_menu.pop(5)
                context['menu'] = user_menu
                context['genres'] = genres
                if 'gen_selected' not in context:
                        context['gen_selected'] = 0
                return context


