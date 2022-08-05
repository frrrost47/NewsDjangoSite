from django.contrib import admin
from .models import News, Category


# admin.site.register(News)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # поля, которые будут видны в админке
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published')
    # поля, которые ссылаются на редактирование модели в админке
    list_display_links = ('id', 'title')
    # поля по которым будет работать поиск в админке (регистр ру поиска важен)
    search_fields = ('title', 'content')
    # поля которые редактируются прям из списка админки
    list_editable = ('is_published',)
    # добавит фильтр по полям в админке
    list_filter = ('is_published', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
