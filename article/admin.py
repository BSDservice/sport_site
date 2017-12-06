from django.contrib import admin
from .models import *
from django.forms import TextInput, Textarea
from django.db import models


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


@admin.register(Recipe)
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


class SupListAdminInline(admin.StackedInline):
    model = SupList
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
    }


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


admin.site.register(Topic)
admin.site.register(Section)

