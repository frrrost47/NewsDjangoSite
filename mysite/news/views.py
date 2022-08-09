"""View controllers"""
from django.shortcuts import render, get_object_or_404
from .models import News, Category


def index(request):
    news = News.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей',
    }
    # шаблон ищется в папке templates по умолчанию
    return render(request, 'news/index.html', context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    context = {'news': news, 'category': category}
    return render(request, 'news/category.html', context)


def view_news(request, news_id):
    #  news_item = News.objects.get(pk=news_id)
    """ если не будет новости по pk, то выскочит исключение 404
    сокращенная запись от
    from django.http import Http404
    try:
        obj = MyModel.objects.get(pk=1)
    except MyModel.DoesNotExist:
        raise Http404('No MyModel matches the given query.') """
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})
