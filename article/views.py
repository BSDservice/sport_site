from django.shortcuts import render


def nutrition(request):
    return render(request, 'article/nutrition/nutrition.html')


def recipe(request):
    return render(request, 'article/nutrition/recipe.html')


def supplement(request):
    return render(request, 'article/nutrition/supplement.html')


def ration(request):
    return render(request,'article/nutrition/ration.html')
