from django.db import models
from django.utils import timezone
from django.urls import reverse


# абстрактный класс статьи
class Article(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, verbose_name='Заголовок', primary_key=True)
    subtitle = models.CharField(max_length=200, verbose_name='Подзаголовок')
    img = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    intro = models.TextField(verbose_name='Вступительная часть')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


# модель для статьи-рецепт
class Recipe(Article):
    t_prepare = models.PositiveSmallIntegerField(verbose_name='Время на подготовку ингридиентов, мин.')
    t_cook = models.PositiveSmallIntegerField(verbose_name='Время приготовления, мин.')

    def get_absolute_url(self):
        return reverse('recipe', args=[str(self.id)])


# таблица ингредиентов для рецепта
class Ingredients(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    item = models.CharField(max_length=100, verbose_name='ингридиент', null=True, blank=True)


# таблица приготовления по шагам к рецепту
class CookingProcess(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    step = models.CharField(max_length=100, verbose_name='шаг', null=True, blank=True)


# модель для статьи-добавки
class Supplement(Article):

    def get_absolute_url(self):
        return reverse('supplement', args=[str(self.id)])


# таблица добавок к статье-добавки
class SupList(models.Model):
    supplement = models.ForeignKey('Supplement', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='название добавки')
    description = models.TextField(verbose_name='описание')


# модель для статьи-рациона
class Ration(Article):
    text1 = models.TextField(verbose_name='Первая часть')
    text2 = models.TextField(verbose_name='Вторая часть')
    text3 = models.TextField(verbose_name='Третья часть')

    def get_absolute_url(self):
        return reverse('diete', args=[str(self.id)])


class GalleryRation(models.Model):
    diete = models.ForeignKey('Ration',on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')

