from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),  # name - имя маршрута(используется чтобы при смене маршрута не менять все шаблоны)
    path('category/<int:category_id>/', get_category, name='category'),  # URL с динамическим id
    path('news/<int:news_id>/', view_news, name='view_news'),  # URL с динамическим id
]