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
    section_stat = Statistic7days.objects.filter(article=obj)
    top7 = max(i.seven_days for i in section_stat)
    top3 = max(i.three_days for i in section_stat)

    subsection_list = Subsection.objects.filter(section__name=section_name)
    return render(request, 'article/section.html', {'obj': obj, 'section_name': section_name,
                                                    'subsection_list': subsection_list, 'section_list': section_list})


def subsection(request, section_name, subsection_name):
    section_list = Section.objects.all()
    obj = Article.objects.filter(section__name=section_name, subsection__name=subsection_name)
    return render(request, 'article/subsection.html', {'subsection_name': subsection_name, 'obj': obj, 'section_list': section_list})


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
            # если имеется, пробуем получить запись из таблици уникальных пользователей. Если такой товарищ отметился
            # и дата статистики не отличается от текущей, то просто отдаем статью. Если дата отличается удалим всех
            # читателей данной статьи и обновим статистику продвинув её вперед.
            if UserList.objects.filter(article__title=article_title).get(user_id=user_id) and stat.date != date.today():
                UserList.objects.filter(article=obj).exclude(user_id=user_id).delete()
                # UserList.objects.create(user_id=user_id, article=obj)
                stat.date = date.today()
                stat.three_days = stat.first + stat.second + stat.third
                stat.seven_days = stat.three_days + stat.fourth + stat.fifth + stat.sixth + stat.seventh
                stat.seventh = stat.sixth
                stat.sixth = stat.fifth
                stat.fifth = stat.fourth
                stat.fourth = stat.third
                stat.third = stat.second
                stat.second = stat.first
                stat.first = 1
                stat.total += 1
                stat.save()
        except UserList.DoesNotExist:                      # получаем ошибку в случае отсутствия
            UserList.objects.create(user_id=user_id, article=obj)  # и создаём запись уникального посетителя
            if stat.date == date.today():                 # таблица уникальных посетителей на сутки
                stat.first += 1                            # пока дата не сменилась, просто инкриментируем поля
                stat.total += 1
                stat.save()
            else:                                          # если дата сменилась, обнулим таблицу уникальных посетителей
                UserList.objects.filter(article=obj).delete()  # чтобы можно было учитывать их посещения.
                stat.date = date.today()                  # ставим сегоднешнюю дату и продвигаем значения в таблице
                stat.three_days = stat.first + stat.second + stat.third
                stat.seven_days = stat.three_days + stat.fourth + stat.fifth + stat.sixth + stat.seventh
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
