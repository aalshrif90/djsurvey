from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^code/$', views.code, name='code'),
    url(r'^background/$', views.background, name='background'),
    url(r'^question/$', views.question, name='question'),
    url(r'^schemashowed/$', views.schemaShowed, name='schemaShowed'),
    url(r'^preference/$', views.prefernceQuetion, name='preference'),
    url(r'^exitQuestion/$', views.exitQuestion, name='exitQuestion'),
    url(r'^print/$', views.printAllQuestions, name='printAllQuestions'),
    url(r'^exit/$', views.exit, name='exit'),
]
