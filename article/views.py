from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from datetime import date
from django.db.models import Max


def index(request):
    section_list = Section.objects.all()
    nutrition3 = Article.objects.filter(section__name='Питание', status=1).order_by('-created_date')[1:4]
    fitness3 = Article.objects.filter(section__name='Фитнес', status=1).order_by('-created_date')[1:4]
    sex3 = Article.objects.filter(section__name='Секс', status=1).order_by('-created_date')[1:4]
    sections = (nutrition3, fitness3, sex3)
    last3 = Article.objects.filter(status=1).order_by('-created_date')[:3]
    top5 = Article.objects.filter(statistic7days__date=date.today(), status=1).order_by('-statistic7days__first')[:5]
    return render(request, 'article/index.html', {'section_list': section_list, 'last3': last3, 'top5': top5,
                                                  'sections': sections})


def section(request, section_name):
    section_list = Section.objects.all()
    subsection_list = Subsection.objects.filter(section__name=section_name)
    obj = Article.objects.filter(section__name=section_name, status=1).order_by('-created_date')
    last = obj.first()
    obj = obj.exclude(title=last)
    top7 = obj.order_by('-statistic7days__seven_days').first()
    top3 = obj.exclude(title=top7).order_by('-statistic7days__three_days').first()
    all_latest = Article.objects.filter(status=1).exclude(title=last, status=0).order_by('-created_date')[:5]

    return render(request, 'article/section.html', {'obj': obj, 'section_name': section_name,
                                                    'subsection_list': subsection_list, 'section_list': section_list,
                                                    'top7': top7, 'top3': top3, 'last': last, 'all_latest': all_latest})


def subsection(request, section_name, subsection_name):
    section_list = Section.objects.all()
    obj = Article.objects.filter(section__name=section_name, subsection__name=subsection_name, status=1)
    return render(request, 'article/subsection.html', {'subsection_name': subsection_name, 'obj': obj, 'section_list': section_list})


def exercise_view(request, exercise):
    obj = get_object_or_404(Exercise, name=exercise)
    return render(request, 'article/exercise.html', {'obj': obj})


def article(request, section_name, subsection_name, article_title):
    # обновление статистики при запросе статьи
    if not request.session.session_key:                    # проверяем наличие ID сессии в запросе
        request.session.save()                             # если нет, сохраням сессию в куки
    user_id = request.session.session_key                  # и достаём его
    obj = get_object_or_404(Article, title=article_title)  # достаем статью
    obj_list = Article.objects.filter(subsection__name=subsection_name)
    top3_week = obj_list.order_by('statistic7days__seven_days')[:3]
    stat = Statistic7days.objects.get_or_create(article=obj)
    stat = Statistic7days.objects.get(article=obj)         # получаем статистику по данной статье
    if user_id:                                            # проверяем наличие ID сессии если нет
        try:                                               # просто отправим статью
            # если имеется, пробуем получить запись из таблици уникальных пользователей. Если такой товарищ отметился
            # и дата статистики не отличается от текущей, то просто отдаем статью. Если дата отличается удалим всех
            # читателей данной статьи и обновим статистику продвинув её вперед.
            if UserList.objects.filter(article__title=article_title).get(user_id=user_id) and stat.date != date.today():
                UserList.objects.filter(article=obj).exclude(user_id=user_id).delete()
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
    # выборка для тренировок
    training_list = False
    training_part = False
    if subsection_name == 'Программы тренировок':
        training_list = Training.objects.filter(article=obj)
        training_part = TrainingPart.objects.filter(training__article=obj)

    return render(request, 'article/article.html', {'obj': obj, 'obj_list': obj_list, 'top3_week': top3_week,
                                                    'training_list': training_list, 'training_part': training_part})
