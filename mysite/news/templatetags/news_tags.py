from django import template
from news.models import Category
from django.db.models import Count

register = template.Library()


#  регистрация кастомного тега
@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


#  регистрация inclusion тега
@register.inclusion_tag('news/list_categories.html')
def show_categories(categories_name='Категории:'):
    # categories = Category.objects.all()
    # добавляет к модели запроса атрибут cnt и фильтрует по нему(в итоге пустые категории не будут отображаться)
    categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    return {'categories': categories, 'categories_name': categories_name}
