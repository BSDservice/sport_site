from django.conf.urls import url
from article import views


urlpatterns = [
    url(r'^питание/$', views.nutrition, name='nutrition'),
    url(r'^питание/рецепты/$', views.listrecipe, name='list_recipe'),
    url(r'^питание/добавки/$', views.listsupplement, name='list_supplement'),
    url(r'^питание/рацион/$', views.listration, name='list_ration'),
    url(r'^питание/рецепты/(?P<pk>w+)$', views.recipe, name='recipe'),
    url(r'^питание/добавки/(?P<pk>w+)$', views.supplement, name='supplement'),
    url(r'^питание/рацион/(?P<pk>w+)$', views.ration, name='ration'),
    url(r'^фитнес/$', views.fitness, name='fitness'),
    url(r'^фитнес/программы тренировок/$', views.listtrenning, name='list_tanning'),
    url(r'^фитнес/кардио$', views.listcardio, name='list_cardio'),
    url(r'^фитнес/выносливость$', views.listendurance, name='list_endurance'),
    url(r'^фитнес/масса$', views.listmassa, name='list_massa'),
    url(r'^фитнес/кардио/(?P<pk>w+)$', views.cardio, name='cardio'),
    url(r'^фитнес/выносливость/(?P<pk>w+)$', views.endurance, name='endurance'),
    url(r'^фитнес/масса/(?P<pk>w+)$', views.massa, name='massa'),
]