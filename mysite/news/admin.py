from django.contrib import admin
from .models import News


# admin.site.register(News)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'is_published')  # поля, которые будут видны в админке
    list_display_links = ('id', 'title')  # поля, которые ссылаются на редактирование модели в админке
    search_fields = ('title', 'content')  # поля по которым будет работать поиск в админке (регистр ру поиска важен)

