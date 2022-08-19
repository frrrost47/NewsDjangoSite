from django.db import models
from django.urls import reverse_lazy


# id и pk создается автоматически
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')  # blank true - не обязательно к заполнению
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    ''' 1) Для использования ImageField django при старте сервера заставит установить 
    доп библиотеку Pillow которая проверяет файлы на изображения.
    2) Придется добавить в settings.py такие свойства:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/' 
    3) Для отладочного режима придется добавить в urls.py "if settings.DEBUG:" где будут использоваться эти 
    константы. Без отладочного режима сервер сам все сделает. '''
    # путь загрузки картинок из админки
    # blank=True - опционально для заполнения
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')  # без default = none
    views = models.IntegerField(default=0)

    ''' Опциональная связь "многие к одному". 
    related_name - обратная связь category_object.news.all() вернет все новости 
    если не определить related_name, то по умолчанию будет:
    category_object.news_set.all() как category_object.<имя модели>_set.all() '''
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                 verbose_name='Категория', related_name='news')

    # в shell принтит объект отображая его title
    def __str__(self):
        return self.title

    ''' такое название функции специальное для джанги (отобразится в админке)
        этот метод сам выстроит маршрут
        благодаря этому методу шаблоны получают ссылку и рендерят страницу категории
        + в админке автоматически добавится кнопка "Смотреть на сайте" 
        Так же является как redirect URL (например когда добавляется новость из формы) '''

    def get_absolute_url(self):
        return reverse_lazy('view_news', kwargs={'pk': self.pk})

    # класс для визуализации админки и пользовательской части
    class Meta:
        verbose_name = 'Новость'  # наименование модели в единственном числе
        verbose_name_plural = 'Новости'  # наименование модели во множественном числе
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    # в shell принтит объект отображая его title
    def __str__(self):
        return self.title

    ''' такое название функции специальное для джанги (отобразится в админке)
        этот метод сам выстроит ссылку category/category_id
        благодаря этому методу шаблоны получают ссылку и рендерят страницу категории
        + в админке автоматически добавится кнопка "Смотреть на сайте" '''

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'category_id': self.pk})

    # класс для визуализации админки и пользовательской части
    class Meta:
        verbose_name = 'Категория'  # наименование модели в единственном числе
        verbose_name_plural = 'Категории'  # наименование модели во множественном числе
        ordering = ['title']


''' Django ORM:
python manage.py shell
from news.models import *
from django.db.models import Q  # для создания условий |(или) &(и) ~(не)
from django.db.models import Avg, Count, Max, Min, StdDev, Sum, Variance # Агрегатные функции
from django.db import connection  # чтобы смотреть обращения к BD (connection.queries)
from django.db import reset_queries # чтобы очистить запросы connection через reset_queries()
from django.db.models import F  # для сравнения и потокобезопасного(?) изменения полей модели
from django.db.models.functions import Length  # использую в разделе Functions:


reset_queries() - очистит массив запросов
connection.queries - покажет какие запросы были выполнены

# С подключением Q
News.objects.filter(Q(pk__in=[5,6] | Q(title__contains='2') & ~Q(pk__lt=4))

# По умолчанию идет условие И
News.objects.filter(pk__in=[5,6], title__contains='2', pk__gt=4) 
News.objects.all()[:3] - получить 3 записи (не поддерживает отрицательные индексы)

.last()
.first()
.distinct() - Оставит только уникальные записи
.aggregate() - агрегатные функции

Aggregate:
# агрегатные функции позволяют делать вычисления
News.objects.aggregate(Min('views'), Max('views')) - вернет словарь с 2 объектами с названиями по умолчанию
News.objects.aggregate(min_views=Min('views'), max_views=Max('views')) - тоже самое с кастомными ключами словаря
News.objects.aggregate(diff=Max('views')-Min('views')) - кастомное вычисление с разницей, по ключу diff
News.objects.aggregate(Sum('views')) - ключ views__sum
News.objects.aggregate(Avg('views')) - среднее значение ключ views__avg
News.objects.aggregate(Count('views'))  

Annotate:
# annotate позволяет делать вычисления в группе записей для count по умолчанию ключ item.news__count либо кастомный cnt
cats = Category.objects.annotate(cnt=Count('news')) 
for item in cats:
    print(item.title, item.cnt) 
cats = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
#  Добавление distinct позволяет посчитать только уникальные значения
News.objects.aggregate(cnt=Count('views', distinct=True))

Values:
# формирует словарь в которых будут только конкретные поля и их связанные объекты (category__title)
News.objects.values('title', 'views', 'category__title').get(pk=1)

F:
# Потокобезопасный способ работы с полями модели?
news = News.objects.git(pk=1)
news.views = F('views') + 1
news.save()

News.objects.filter(content__icontains=F('title'))


Functions:
# Дополнительные функции можно найти в документации
news = News.objects.annotate(length=Length('title')).all()

SQL raw:
# Прямые SQL запросы
news = News.objects.raw('SELECT * FROM news_news') 
# при получении полей, поле id обязательное 
news = News.objects.raw('SELECT id, title FROM news_news')
news = News.objects.raw('SELECT * FROM news_news WHERE title = "News 5"')
'''