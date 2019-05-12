from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pcode/$', views.pcode, name='pcode'),
    url(r'^background/$', views.background, name='background'),
    url(r'^question/$', views.question, name='question'),
    url(r'^showProgramCode/$', views.showProgramCode, name='showProgramCode'),
    url(r'^exit/$', views.exit, name='exit'),
]