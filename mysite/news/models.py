from django.db import models


# id и pk создается автоматически
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')  # blank true - не обязательно к заполнению
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    ''' 
    1) Для использования ImageField django при старте сервера заставит установить 
    доп библиотеку Pillow которая проверяет файлы на изображения.
    2) Придется добавить в settings.py такие свойства:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/' 
    3) Для отладочного режима придется добавить в urls.py "if settings.DEBUG:" где будут использоваться эти 
    константы. Без отладочного режима сервер сам все сделает. 
    '''
    # путь загрузки картинок из админки
    # blank=Trui - опционально для заполнения
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')  # без default = none

    # в shell принтит объект отображая его title
    def __str__(self):
        return self.title

    # класс для визуализации админки и пользовательской части
    class Meta:
        verbose_name = 'Новость'  # наименование модели в единственном числе
        verbose_name_plural = 'Новости'  # наименование модели во множественном числе
        ordering = ['-created_at']

