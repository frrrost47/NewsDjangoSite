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

    ''' Опциональная связь "многие к одному" '''
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

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
