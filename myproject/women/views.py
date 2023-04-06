from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *

menu = [{'title': "Головна Сторінка", 'url_name': 'home'},
        {'title': "Про сайт", 'url_name': 'about'},
        {'title': "Додати статтю", 'url_name': 'add_page'},
        {'title': "Зворотній зв'язок", 'url_name': 'contact'},
        {'title': "Увійти", 'url_name': 'login'}
]

def index(request):
    posts = Women.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница'
    }
    return render(request, 'women/index.html', context=context)

def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'Про сайт'})

def addpage(request):
    return HttpResponse("Додання статті")

def contact(request):
    return HttpResponse("Зворотній зв'язок")

def login(request):
    return HttpResponse("Авторизація")

def show_post(request, post_id):
    return HttpResponse(f"Відображення статті з id = {post_id}")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')