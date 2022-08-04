from django.db import models


class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)  # blank true - не обязательно к заполнению
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ''' Для использования ImageField django при старте сервера заставит установить доп библиотеку'''
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')  # путь загрузки картинок
    is_published = models.BooleanField(default=True)  # без default = none
