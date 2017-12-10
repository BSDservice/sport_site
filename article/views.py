from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from datetime import date


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
    # обновление статистики при запросе статьи
    if not request.session.session_key:                    # проверяем наличие ID сессии в запросе
        request.session.save()                             # если нет, сохраням сессию в куки
    user_id = request.session.session_key                  # и достаём его
    obj = get_object_or_404(Article, title=article_title)  # достаем статью
    stat = Statistic7days.objects.get_or_create(article=obj)
    stat = Statistic7days.objects.get(article=obj)         # получаем статистику по данной статье
    if user_id:                                            # проверяем наличие ID сессии если нет
        try:                                               # просто отправим статью
            # если имеется, пробуем получить запись из таблици уникальных пользователей. Если такой товарищ сегодня
            UserList.objects.filter(article__title=article_title).get(
                                               user_id=user_id)  # просматривал эту статью, то просто отдадим ему её
        except UserList.DoesNotExist:                      # получаем ошибку в случае отсутствия
            UserList.objects.create(user_id=user_id, article=obj)  # и создаём запись уникального посетителя
            if stat.today == date.today():                 # таблица уникальных посетителей на сутки
                stat.first += 1                            # пока дата не сменилась, просто инкриментируем поля
                stat.total += 1
                stat.save()
            else:                                          # если дата сменилась, обнулим таблицу уникальных посетителей
                UserList.objects.all().delete()            # чтобы можно было учитывать их посещения.
                stat.today = date.today()                  # ставим сегоднешнюю дату и продвигаем значения в таблице
                stat.seventh = stat.sixth                  # с статистекой вперёд
                stat.sixth = stat.fifth
                stat.fifth = stat.fourth
                stat.fourth = stat.third
                stat.third = stat.second
                stat.second = stat.first
                stat.first = 1
                stat.total += 1
                stat.save()

    return render(request, 'article/article.html', {'obj': obj})


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