from django.urls import path
from article import views


urlpatterns = [
    path('', views.index, name='index'),
    path('питание/', views.nutrition, name='nutrition'),
    path('питание/рецепты/', views.list_recipe, name='list_recipe'),
    path('питание/добавки/', views.list_supplement, name='list_supplement'),
    path('питание/рацион/', views.list_ration, name='list_ration'),
    path('питание/рецепты/(<str:title>)', views.recipe, name='recipe'),
    path('питание/добавки/(<str:title>)', views.supplement, name='supplement'),
    path('питание/рацион/<str:title>/', views.ration, name='ration'),
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
