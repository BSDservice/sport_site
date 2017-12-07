from django.db import models
from django.utils import timezone
from django.urls import reverse


# разделы(питание, фитнес, секс)
class Section(models.Model):
    name = models.CharField(max_length=200, verbose_name='Раздел')
    description = models.TextField(verbose_name='Описание раздела')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Список разделов'
        db_table = 'section'


class Subsection(models.Model):
    name = models.CharField(max_length=200, verbose_name='Подраздел')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подраздел'


# тематические ветвления
class Topic(models.Model):
    name = models.CharField(max_length=50, verbose_name="Тематика")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'topic'
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрика'


# абстрактный класс статьи из араздела питание
class Article(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, null=True,blank=True, on_delete=models.SET_NULL)
    subsection = models.ForeignKey(Subsection, null=True,blank=True, on_delete=models.SET_NULL)
    topic = models.ManyToManyField(Topic, verbose_name='Рубрика')
    title = models.CharField(max_length=200, verbose_name='Заголовок', unique=True)
    subtitle = models.CharField(max_length=200, verbose_name='Подзаголовок')
    img = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    intro = models.TextField(verbose_name='Вступительная часть')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    PUBLIC_STATUS = (
        (0, 'Черновик'),
        (1, 'Готова к публикации')
    )
    status = models.SmallIntegerField(choices=PUBLIC_STATUS, default=0, verbose_name='Статус')

    text = models.TextField(verbose_name='Текст статьи')
    time = models.TimeField(verbose_name='Время')

    def publish(self):
        self.published_date = timezone.now()
        self.status = 1
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Статья'
        verbose_name_plural = u'Список статей'


# таблица ингредиентов для рецепта
class Ingredient(models.Model):
    recipe = models.ForeignKey(Article, on_delete=models.CASCADE)
    item = models.CharField(max_length=100, verbose_name='ингридиент', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'ingredient'
        verbose_name = u'Ингридиент'
        verbose_name_plural = u'Ингридиенты'


# таблица приготовления по шагам к рецепту
class CookingProcess(models.Model):
    recipe = models.ForeignKey(Article, on_delete=models.CASCADE)
    step = models.CharField(max_length=500, verbose_name='шаг', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'cookproc'
        verbose_name = u'Шаг'
        verbose_name_plural = u'Процесс приготовления'


# таблица добавок к статье-добавки
class SupList(models.Model):
    supplement = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='название добавки')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'suplist'
        verbose_name = u'Список добавок'
        verbose_name_plural = u'Список добавок'


# галерея к рациону
class Gallery(models.Model):
    ration = models.ForeignKey(Article,on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'gallery'
        verbose_name = u'Изображение'
        verbose_name_plural = u'Галерея'



# КОНЕЦ РАЗДЕЛА ПИТЬАНИЕ
