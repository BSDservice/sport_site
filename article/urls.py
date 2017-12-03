from django.conf.urls import url
from article import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^питание/$', views.nutrition, name='nutrition'),
    url(r'^питание/рецепты/$', views.list_recipe, name='list_recipe'),
    url(r'^питание/добавки/$', views.list_supplement, name='list_supplement'),
    url(r'^питание/рацион/$', views.list_ration, name='list_ration'),
    url(r'^питание/рецепты/(?P<pk>\w+)$', views.recipe, name='recipe'),
    url(r'^питание/добавки/(?P<pk>\w+)$', views.supplement, name='supplement'),
    url(r'^питание/рацион/(?P<pk>\w+)$', views.ration, name='ration'),
]
'''
urlpatterns += [url(r'^фитнес/$', views.fitness, name='fitness'),
    url(r'^фитнес/программы тренировок/$', views.listtrenning, name='list_tanning'),
    url(r'^фитнес/кардио$', views.listcardio, name='list_cardio'),
    url(r'^фитнес/выносливость$', views.listendurance, name='list_endurance'),
    url(r'^фитнес/масса$', views.listmassa, name='list_massa'),
    url(r'^фитнес/кардио/(?P<pk>w+)$', views.cardio, name='cardio'),
    url(r'^фитнес/выносливость/(?P<pk>w+)$', views.endurance, name='endurance'),
    url(r'^фитнес/масса/(?P<pk>w+)$', views.massa, name='massa'),
]
'''
