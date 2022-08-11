from django import forms
from .models import Category


# Форма не связанная на прямую с моделью
class NewsForm(forms.Form):
    # widget влияет на внешний вид поля
    title = forms.CharField(max_length=150, label='Название:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст:', required=False, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 5
        }))
    is_published = forms.BooleanField(label='Опубликовано:', initial=True)
    category = forms.ModelChoiceField(empty_label=None, label='Категория:', queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
