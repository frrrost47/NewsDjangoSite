"""View controllers"""
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from .forms import NewsForm, UserRegisterForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.contrib import messages


# регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def login(request):
    return render(request, 'news/login.html')


def test(request):
    objects = ['join1', 'paul2', 'george3', 'ringo4', 'join5', 'paul6', 'george7']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)  # если в URL не будет 'page', то присвоит 1
    page_obj = paginator.get_page(page_num)  # .get_page не вызывает исключения .page вызывает
    return render(request, 'news/test.html', {'page_obj': page_obj})


# Все новости
class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'  # название объектов БД для шаблона
    mixin_prop = 'Hello world'
    paginate_by = 2  # пагинация страниц по 2 записи

    # queryset = News.objects.select_related('category')

    # дополнительные атрибуты для шаблона(не рекомендуется для динамичных данных)
    # extra_context = {'title': 'Главная'}

    # Метод переопределяется, чтобы получить контекст и наполнить его дополнительными данными как extra_context?
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    # Фильтр данных которые описывает этот класс
    def get_queryset(self):
        # .select_related - улучшает качество SQL запроса(связанные модели выполнятся одним запросом)
        return News.objects.filter(is_published=True).select_related('category')


# Новости отфильтрованные по категории
class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False  # запрет показа пустых списков для выдачи 404 ошибки
    paginate_by = 2  # пагинация страниц по 2 записи

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)

    # Метод переопределяется, чтобы получить контекст и наполнить его дополнительными данными как extra_context?
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context


class ViewNews(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'
    # py_url_kwarg = 'news_id'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm  # связываем класс с формой
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')  # redirect url
    login_url = reverse_lazy('/admin')  # идет от LoginRequiredMixin будет перебрасывать сюда non admin users
    # raise_exception = True # идет от LoginRequiredMixin будет вызывать исключение 403 для non admin users


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {'news': news, 'category': category}
#     return render(request, 'news/category.html', context)
#
#
# def view_news(request, news_id):
#     #  news_item = News.objects.get(pk=news_id)
#     """ если не будет новости по pk, то выскочит исключение 404
#     сокращенная запись от
#     from django.http import Http404
#     try:
#         obj = MyModel.objects.get(pk=1)
#     except MyModel.DoesNotExist:
#         raise Http404('No MyModel matches the given query.') """
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})
#
#
# # Контроллер с формой, которая связанна с моделью
# def add_news(request):
#     if request.method == 'POST':
#         # таким образом заполнили форму через POST
#         form = NewsForm(request.POST)
#         # если форма прошла валидацию
#         if form.is_valid():
#             # form.cleaned_data - данные с которыми можно работать(например для SQL запросов)
#             news = form.save()
#             # после сохранения перекинут на страницу новости
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})


''' Контроллер с формой, которая НЕ связанна с моделью'''
'''
def add_news(request):
    if request.method == 'POST':
        # таким образом заполнили форму через POST
        form = NewsForm(request.POST)
        # если форма прошла валидацию
        if form.is_valid():
            # form.cleaned_data - данные с которыми можно работать(например для SQL запросов)
            # ** - распаковка словаря
            # .create сохранит новость и вернет ее в переменную
            news = News.objects.create(**form.cleaned_data)
            # после сохранения перекинут на страницу новости
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})
'''
