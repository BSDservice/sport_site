from django.db import models
from django.utils import timezone
from django.urls import reverse


# разделы(питание, фитнес, секс)
class Section(models.Model):
    name = models.CharField(max_length=200, verbose_name='Раздел', unique=True)
    description = models.TextField(verbose_name='Описание раздела')

    def get_url(self):
        return self.name.lower()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Список разделов'
        db_table = 'section'


# подразделы
class Subsection(models.Model):
    name = models.CharField(max_length=200, verbose_name='Подраздел', unique=True)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)

    def get_url(self):
        return self.name.lower()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подраздел'
        verbose_name_plural = 'Подразделы'


# тематические ветвления
class Topic(models.Model):
    name = models.CharField(max_length=50, verbose_name="Тематика")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'topic'
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрика'


# таблица уникальных посещений на сутки
class UserList(models.Model):
    user_id = models.CharField(max_length=64)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


# статистика на семь дней
class Statistic7days(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Дата последнего посещения')
    first = models.PositiveSmallIntegerField(verbose_name='сегодня', default=0)
    second = models.PositiveSmallIntegerField(verbose_name='Вчера', default=0)
    third = models.PositiveSmallIntegerField(verbose_name='Позавчера', default=0)
    fourth = models.PositiveSmallIntegerField(verbose_name='Три дня назад', default=0)
    fifth = models.PositiveSmallIntegerField(verbose_name='Четыре дня назад', default=0)
    sixth = models.PositiveSmallIntegerField(verbose_name='Пять дней назад', default=0)
    seventh = models.PositiveSmallIntegerField(verbose_name='Шесть дней назад', default=0)
    total = models.PositiveIntegerField(verbose_name='Всего просмотров', default=0)
    article = models.OneToOneField('Article', on_delete=models.CASCADE)
    three_days = models.PositiveIntegerField(verbose_name='просмотров за три дня', default=0)
    seven_days = models.PositiveIntegerField(verbose_name='просмотров за семь дней', default=0)

    def __str__(self):
        return self.article.title


# РАЗДЕЛ ПИТАНИЯ
# класс статьи
class Article(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.SET_NULL)
    subsection = models.ForeignKey(Subsection, null=True, blank=True, on_delete=models.SET_NULL)
    topic = models.ManyToManyField(Topic, verbose_name='Рубрика')
    title = models.CharField(max_length=200, verbose_name='Заголовок', unique=True)
    subtitle = models.CharField(max_length=200, verbose_name='Подзаголовок')
    img = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    text = models.TextField(verbose_name='Текст статьи')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    PUBLIC_STATUS = (
        (0, 'Черновик'),
        (1, 'Готова к публикации')
    )
    status = models.SmallIntegerField(choices=PUBLIC_STATUS, default=0, verbose_name='Статус')
    time = models.SmallIntegerField(blank=True, null=True, verbose_name='Время')

    def get_url(self):
        return (self.subsection.name + '/' + self.title).lower()

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


# РАЗДЕЛ ФИТНЕСА
# модель упражнения
class Exercise(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название упражнения', unique=True)
    equipment = models.CharField(max_length=100, verbose_name='Спортинвентарь', unique=True)
    body_parts = models.CharField(max_length=100, verbose_name='Прокачиваемая часть тела', unique=True)
    img = models.ImageField(null=True, blank=True, verbose_name='Изображение')


# иллюстрации с описаниями к упражнениям
class GalleryExercise(models.Model):
    exercise = models.ForeignKey(Exercise,on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'g_exercise'
        verbose_name = u'Изображение'
        verbose_name_plural = u'Галерея'


# упражнение в тренировке
class TrainingPart(models.Model):
    exercise = models.ForeignKey(on_delete=models.CASCADE, verbose_name='Упражнение')
    sets = models.PositiveSmallIntegerField(verbose_name='Колличество сетов')
    reps = models.PositiveSmallIntegerField(verbose_name='Колличество повторений в каждом сете')
    rest = models.TimeField(verbose_name='Время отдыха между сетами')
    comment = models.CharField(max_length=200, verbose_name='Комментарий')


class Training(models.Model):
    article = models.ForeignKey(Article,verbose_name='Статья')
    name = models.CharField(max_length=100, verbose_name='Название тренировки', unique=True)
    exercise = models.ForeignKey(TrainingPart, verbose_name='Упражнение')