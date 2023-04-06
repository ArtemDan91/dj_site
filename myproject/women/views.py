from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *

menu = ['Про сайт', 'Додати статтю', 'Зворотній звязок', 'Увійти']
def index(request):
    posts = Women.objects.all()
    return render(request, 'women/index.html', {'posts': posts, 'menu': menu, 'title': 'Головна сторінка'})

def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'Про сайт'})

def categories(request, id):
    if (request.GET):
        print(request.GET)
    return HttpResponse(f"<h1>Статті по категоріям</h1><p>{id}</p>")

def archive(request, year):
    if int(year) > 2023:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Статті по категоріям</h1><p>{year}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')