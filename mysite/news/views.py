"""View controllers"""

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    print(dir(request))
    return HttpResponse('Hello world')


def test(request):
    return HttpResponse('Тестовая страница')