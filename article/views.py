from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from datetime import date
from django.http import HttpResponse


def index(request):
    section_list = Section.objects.all()
    subsection_list = Subsection.objects.all()
    sections = []
    for section in section_list:
        try:
            q = Article.objects.filter(section__name=section, status=1).order_by('-created_date')[0:4]
            if len(q) > 0: sections.append(q)
        except Article.DoesNotExist:
            pass
    last3 = Article.objects.filter(status=1).order_by('-created_date')[:3]
    top5 = Article.objects.filter(statistic7days__date=date.today(), status=1).order_by('-statistic7days__first')[:5]
    return render(request, 'article/index.html', {'section_list': section_list, 'last3': last3, 'top5': top5,
                                                  'sections': sections, 'subsection_list': subsection_list,})


def section(request, section_name):
    section_list = Section.objects.all()
    #full_subsection_list = Subsection.objects.all()
    subsection_list = Subsection.objects.all()  #full_subsection_list.filter(section__name=section_name)
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
        return render(request, 'article/list_for_section.html', {'obj': next_objects, 'section_name': section_name})
    return render(request, 'article/section.html', {'obj': next_objects, 'section_name': section_name,
                                                    'subsection_list': subsection_list, 'section_list': section_list,
                                                    'top7': top7, 'top3': top3, 'last': last, 'all_latest': all_latest,
                                                    'max': max})


def subsection(request, section_name, subsection_name):
    section_list = Section.objects.all()
    #full_subsection_list = Subsection.objects.all()
    subsection_list = Subsection.objects.all()  #full_subsection_list.filter(section__name=section_name)
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
    # выборка для тренировок и рецептов
    training_list = False
    training_part = False
    ingredients = False
    cooking_proc =False
    gallery = False
    page = request.GET.get('page')
    if subsection_name == 'Программы тренировок' and page is None:
        training_list = Training.objects.filter(article=obj)
        training_part = TrainingPart.objects.filter(training__article=obj).order_by('order')
    if subsection_name == 'Рецепты':
        try:
            ingredients = Ingredient.objects.get(recipe=obj)
        except Ingredient.DoesNotExist:
            ingredients = False
        try:
            cooking_proc = CookingProcess.objects.get(recipe=obj)
        except CookingProcess.DoesNotExist:
            cooking_proc = False
        if Gallery.objects.filter(article=obj):
            gallery = True
        else:
            gallery = False

    if page is not None:
        page = int(page)
        next_article = obj_list[page]
        if subsection_name == 'Программы тренировок':
            training_list = Training.objects.filter(article=next_article)
            training_part = TrainingPart.objects.filter(training__article=next_article).order_by('order')
        if subsection_name == 'Рецепты':
            try:
                ingredients = Ingredient.objects.get(recipe=next_article)
            except Ingredient.DoesNotExist:
                ingredients = False
            try:
                cooking_proc = CookingProcess.objects.get(recipe=next_article)
            except CookingProcess.DoesNotExist:
                cooking_proc = False
            if Gallery.objects.filter(article=next_article):
                gallery = True
            else:
                gallery = False

        return render(request, 'article/article.html', {'obj': next_article, 'section_name': section_name,
                                                        'subsection_list': subsection_list, 'ingredients': ingredients,
                                                        'cooking_proc': cooking_proc, 'subsection_name': subsection_name,
                                                        'training_list': training_list, 'training_part': training_part,
                                                        'section_list': section_list, 'gallery': gallery,})

    return render(request, 'article/article_list.html', {'obj': obj, 'obj_list': obj_list,
                                                         'top3_week': top3_week, 'section_list': section_list,
                                                         'subsection_list': subsection_list, 'section_name': section_name,
                                                         'ingredients': ingredients, 'gallery': gallery, 'max': obj_list.__len__(),
                                                         'cooking_proc': cooking_proc, 'subsection_name': subsection_name,
                                                         'article_title': article_title, 'training_list': training_list,
                                                         'training_part':training_part})


def gallery(request, article_title):
    obj = get_object_or_404(Article, title=article_title)
    gallery_set = get_list_or_404(Gallery, article=obj)
    return render(request, 'article/gallery.html', {'article_title': article_title, 'gallery_set':gallery_set})

def search(request):
    temp = request.GET.get('search')
    srch = Article.objects.filter(text__contains=temp)
    print(temp)
    print(srch)
    return render(request, 'article/search.html', {'srch': srch,})
