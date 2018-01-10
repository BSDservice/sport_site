from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from datetime import date
from django.http import HttpResponse


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
    obj_or_404 = get_list_or_404(obj)
    last = obj.first()
    obj = obj.exclude(title=last)
    top7 = obj.order_by('-statistic7days__seven_days').first()
    top3 = obj.exclude(title=top7).order_by('-statistic7days__three_days').first()
    all_latest = Article.objects.filter(status=1).exclude(title=last, status=0).order_by('-created_date')[:5]
    paginator = Paginator(obj_or_404, 3)
    page = request.GET.get('page')
    next_objects = paginator.get_page(page)
    max = paginator.num_pages
    if page is not None and int(page) > 1:
        print(next_objects)
        return render(request, 'article/list_for_section.html', {'obj': next_objects, 'section_name': section_name})
    return render(request, 'article/section.html', {'obj': next_objects, 'section_name': section_name,
                                                    'subsection_list': subsection_list, 'section_list': section_list,
                                                    'top7': top7, 'top3': top3, 'last': last, 'all_latest': all_latest,
                                                    'max': max})


def subsection(request, section_name, subsection_name):
    section_list = Section.objects.all()
    subsection_list = Subsection.objects.filter(section__name=section_name)
    obj = Article.objects.filter(section__name=section_name, subsection__name=subsection_name, status=1).order_by('-created_date')
    obj_or_404 = get_list_or_404(obj)
    paginator = Paginator(obj_or_404, 3)
    page = request.GET.get('page')
    next_objects = paginator.get_page(page)
    max = paginator.num_pages
    if page is not None and int(page) > 1:
        return render(request, 'article/list_for_section.html', {'obj': next_objects, 'section_name': section_name,
                                                     'subsection_name': subsection_name})
    return render(request, 'article/subsection.html', {'subsection_name': subsection_name, 'obj': next_objects,
                                                       'section_list': section_list, 'subsection_list': subsection_list,
                                                       'section_name': section_name, 'max': max})


def exercise_view(request, exercise):
    section_list = Section.objects.all()
    obj = get_object_or_404(Exercise, name=exercise)
    obj_gallery = GalleryExercise.objects.filter(exercise__name=exercise)
    top3_week = Article.objects.order_by('statistic7days__seven_days')[:3]
    return render(request, 'article/exercise.html', {'obj': obj, 'obj_gallery': obj_gallery, 'top3_week': top3_week,
                                                     'section_list': section_list})


def article(request, section_name, subsection_name, article_title):
    subsection_list = Subsection.objects.filter(section__name=section_name)
    section_list = Section.objects.all()
    # обновление статистики при запросе статьи
    if not request.session.session_key:                    # проверяем наличие ID сессии в запросе
        request.session.save()                             # если нет, сохраням сессию в куки
    user_id = request.session.session_key                  # и достаём его
    obj = get_object_or_404(Article, title=article_title)  # достаем статью
    obj_list = Article.objects.filter(subsection__name=subsection_name).exclude(title=article_title).order_by('-created_date')
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
    ingredients = False
    cooking_proc =False
    if subsection_name == 'Программы тренировок':
        training_list = Training.objects.filter(article=obj)
        training_part = TrainingPart.objects.filter(training__article=obj).order_by('order')
    if subsection_name == 'Рецепты':
        ingredients = Ingredient.objects.get(recipe=obj)
        cooking_proc = CookingProcess.objects.get(recipe=obj)

    page = request.GET.get('page')
    if page is not None:
        print(obj_list[page])
        return render(request, 'article/article.html', {'obj': obj_list[page], 'section_name': section_name, 'section_list': section_list,
                                                        'subsection_list': subsection_list, 'ingredients': ingredients,
                                                        'cooking_proc': cooking_proc, 'subsection_name': subsection_name,})
    return render(request, 'article/article_list.html', {'next_obj': obj_list[0], 'obj': obj, 'obj_list': obj_list, 'top3_week': top3_week,
                                                         'section_list': section_list, 'subsection_list': subsection_list,
                                                         'section_name': section_name, 'ingredients': ingredients,
                                                         'cooking_proc': cooking_proc, 'max': obj_list.__len__(), 'subsection_name': subsection_name,
                                                         'article_title': article_title, 'training_list': training_list, 'training_part':training_part})

"""
def article_next(request, section_name, subsection_name, article_title):
    obj = Article.objects.filter(section=section_name, subsection=subsection_name).exclude(title=article_title).order_by('-created_date')
    paginator = Paginator(obj,1)
    page = request.GET.get('page')
    next_objects = paginator.get_page(page)
    return render(request, 'article/article.html', {'obj_next': next_objects})
"""