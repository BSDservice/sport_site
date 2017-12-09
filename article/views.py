from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *


def index(request):
    section_list = Section.objects.all()
    return render(request, 'article/index.html', {'section_list': section_list})


def section(request, section_name):
    section_list = Section.objects.all()
    obj = Article.objects.filter(section__name=section_name)
    subsection_list = Subsection.objects.filter(section__name=section_name)
    return render(request, 'article/section.html', {'obj': obj, 'section_name': section_name,
                                                    'subsection_list': subsection_list, 'section_list': section_list})


def subsection(request, section_name, subsection_name):
    return render(request, 'article/subsection.html')


def article(request, section_name, subsection_name, article_title):
    return render(request, 'article/article.html')



'''
ПРИМЕР

from django.shortcuts import render
from django.views import generic
from .models import Clothes, Author
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def index(request):
    clothes = Clothes.objects.all()
    author = Author.objects.first()
    clothes_list = []
    a = len(clothes)//3
    n = 0
    y = 0
    for i in range(a+1):
        clothes_list.append([])
        clothes_list[y].append(clothes[n])
        n += 1
        if n >= len(clothes):
            break
        clothes_list[y].append(clothes[n])
        n += 1
        if n >= len(clothes):
            break
        clothes_list[y].append(clothes[n])
        n += 1
        if n >= len(clothes):
            break
        y += 1
    elem = 2
    def paginated():
        if elem < len(clothes_list):
            return True
        else:
            return False
    paginator = Paginator(clothes_list, elem)
    page = request.GET.get('page')
    try:
        clothes_page = paginator.page(page)
    except PageNotAnInteger:
        clothes_page = paginator.page(1)
    except EmptyPage:
        clothes_page = paginator.page(paginator.num_pages)
    return render(request, 'clothes_list.html', context={'clothes_page': clothes_page, 'author': author, 'paginated': paginated()})


class ClothesDetailView(generic.DetailView):
    model = Clothes
'''


def list_ration(request):
    return render(request, 'article/nutrition/list-ration.html')