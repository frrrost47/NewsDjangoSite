from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import News, Category


# admin.site.register(News)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # поля, которые будут видны в админке
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo')
    # поля, которые ссылаются на редактирование модели в админке
    list_display_links = ('id', 'title')
    # поля по которым будет работать поиск в админке (регистр ру поиска важен)
    search_fields = ('title', 'content')
    # поля которые редактируются прям из списка админки
    list_editable = ('is_published',)
    # добавит фильтр по полям в админке
    list_filter = ('is_published', 'category')
    # список полей который нужны внутри нашей новости
    fields = ('title', 'content', 'photo', 'get_photo', 'is_published', 'views',
              'category', 'created_at', 'updated_at')
    # чтобы не было ошибки надо указать какие поля не редактируемые
    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at')
    # кнопки сохранения будут не только внизу страницы, но и наверху
    save_on_top = True

    # эта функция указана в свойстве list_display
    # mark_safe - помечает данную строку как html код и никак ее не экранирует
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{ obj.photo.url }" width="75">')
        else:
            return '-'

    # название колонки get_photo будет отображаться как 'Миниатюра'
    get_photo.short_description = 'Миниатюра'



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
