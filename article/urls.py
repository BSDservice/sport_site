from django.urls import path
from article import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:section_name>/', views.section, name='section'),
    path('<str:section_name>/<str:subsection_name>/', views.subsection, name='subsection'),
    path('<str:section_name>/<str:subsection_name>/<str:article_title>', views.article, name='article'),
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
