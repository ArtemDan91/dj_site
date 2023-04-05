from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect


def index(request):
    return HttpResponse("Сторінка додатку women")

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