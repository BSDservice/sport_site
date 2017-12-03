from django.shortcuts import render
from .models import *


def index(request):
    return render(request, 'article/index.html')


def nutrition(request):
    return render(request, 'article/nutrition/nutrition.html')


def recipe(request):
    return render(request, 'article/nutrition/recipe.html')


def supplement(request):
    return render(request, 'article/nutrition/supplement.html')


def ration(request, pk):
    obj = Ration.objects.get(pk)
    print(type(obj.title))
    return render(request, 'article/nutrition/ration.html',{'title': obj.title})


def list_recipe(request):
    return render(request, 'article/nutrition/list-recipe.html')


def list_supplement(request):
    return render(request, 'article/nutrition/list-supplement.html')


def list_ration(request):
    return render(request, 'article/nutrition/list-ration.html')