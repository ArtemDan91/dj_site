from django.db.models import Count

from .models import *

menu = [{'title': "Головна Сторінка", 'url_name': 'home'},
        {'title': "Про сайт", 'url_name': 'about'},
        {'title': "Додати статтю", 'url_name': 'add_page'},
        {'title': "Зворотній зв'язок", 'url_name': 'contact'},
        {'title': "Увійти", 'url_name': 'login'}
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(total=Count('women'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(2)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context