from django.contrib import admin
from .models import *
from django.forms import TextInput, Textarea
from django.db import models
from django import forms


admin.site.register(Topic)
admin.site.register(Section)
admin.site.register(Gallery)
admin.site.register(Subsection)
admin.site.register(UserList)
admin.site.register(GalleryExercise)
admin.site.register(TrainingPart)
admin.site.register(BodyParts)


@admin.register(Statistic7days)
class Statistic7daysAdmin(admin.ModelAdmin):
    readonly_fields = ('date', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'article', 'total', )
    list_display = ('article', 'date', 'first', 'total', )
    list_filter = ('date', )


class IngredientAdminInline(admin.StackedInline):
    model = Ingredient
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
    }


class CookingProcessAdminInline(admin.StackedInline):
    model = CookingProcess
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
    }


class SupListAdminInline(admin.StackedInline):
    model = SupList
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
    }


class GalleryInline(admin.StackedInline):
    model = Gallery
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class GalleryExerciseInline(admin.StackedInline):
    model = GalleryExercise
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class TrainingPartInline(admin.TabularInline):
    model = TrainingPart
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '15'})},
    }


class TrainingInline(admin.StackedInline):
    model = Training


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'created_date')
    list_filter = ('section', 'subsection')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    search_fields = ('title', 'intro')
    inlines = [IngredientAdminInline, CookingProcessAdminInline, GalleryInline, TrainingInline]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment')
    list_filter = ('equipment', 'body_parts')
    search_fields = ('name',)
    inlines = [GalleryExerciseInline]


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('name', 'article',)
    search_fields = ('name', 'article',)
    inlines = [TrainingPartInline]




'''
admin.site.register(Article)
class RecipeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    # prepopulated_fields = {'': ('',),}  #В качестве входного параметра принимает словарь (dict), в котором в качестве ключей указаны имена заполняемых полей, а в качестве значений кортежи (tuple), в которых перечисляются поля, на основе которых будет происходить заполнение.
    # list_display = () #Указывает, какие поля модели будут отображаться в списке.
    # list_display_links = () # Указывает, какие поля из списка будут представлятся в качестве ссылок для входа в редактирование.
    list_filter = ('status',) #В нем перечисляются поля, по которым можно будет выполнить отбор записей.
    # date_hierarchy = 'created_at' #Указывает поле, по которому определяется иерархия по дате. Это ещё один механизм отбора, работает исключительно с датами, причем с только с одной.
    search_fields = ('title', 'intro')
    # exclude = () #fields и exclude. Будьте осторожны с настройкой fields! Когда она появляется, админка перестает выводить все без исключения поля, а выводит только те, которые перечислены в этом свойстве. В качестве альтернативы используется свойство exclude, в нем перечисляются все поля, которые не должны отображаться.
    # fieldsets = ((None, {'fields': (,)}),(None, {'fields': (,)}),) #Принимает в качестве значения кортеж из кортежей (извините за тавталогию). В кортеже первым элементом должно идти название группы, а вторым словарь из параметров группы. Одним из параметров является fields, в котором перечисляются выводимые поля. Названием группы может также являться None, тогда группа выводится без названия.
    inlines = [IngredientAdminInline, CookingProcessAdminInline]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass





@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    search_fields = ('title', 'intro')
    inlines = [SupListAdminInline]


class GalleryInline(admin.StackedInline):
    model = Gallery
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


@admin.register(Ration)
class RationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    search_fields = ('title', 'intro')
    inlines = [GalleryInline]

'''

