from django.db import models


# id и pk создается автоматически
class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)  # blank true - не обязательно к заполнению
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ''' 
    1) Для использования ImageField django при старте сервера заставит установить 
    доп библиотеку Pillow которая проверяет файлы на изображения.
    2) Придется добавить в settings.py такие свойства:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/' 
    3) Для отладочного режима придется добавить в urls.py "if settings.DEBUG:" где будут использоваться эти 
    константы. Без отладочного режима сервер сам все сделает.
    '''
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')  # путь загрузки картинок
    is_published = models.BooleanField(default=True)  # без default = none

    # в shell принтит объект отображая его title
    def __str__(self):
        return self.title
