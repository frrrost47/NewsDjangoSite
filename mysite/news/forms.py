from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='Максимум 150 символов',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # Виджеты добавляют атрибуты на поля формы меняя внешний вид
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control', 'rows': '5'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control', 'rows': '5'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control', 'rows': '5'}),
        # }


class NewsForm(forms.ModelForm):
    class Meta:
        # Связывает форму и модель
        model = News
        # Поля которые необходимо отобразить в форме = '__all__' - все поля
        fields = ['title', 'content', 'is_published', 'category']
        # Виджеты добавляют атрибуты на поля формы меняя внешний вид
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    # Кастомный валидатор - проверяет чтобы не было цифр в начале строки title
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title


''' forms.Form - Форма не связанная на прямую с моделью. Обычно применяется когда данные не надо сохранять в БД. 
Например для отправки emails '''
'''
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
'''
