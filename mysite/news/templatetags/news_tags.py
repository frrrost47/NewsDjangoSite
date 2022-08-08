from django import template
from news.models import Category

register = template.Library()


#  регистрация кастомного тега
@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


#  регистрация inclusion тега
@register.inclusion_tag('news/list_categories.html')
def show_categories(categories_name='Категории:'):
    categories = Category.objects.all()
    return {'categories': categories, 'categories_name': categories_name}
