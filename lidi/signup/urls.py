from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from . import views

app_name = 'signup'

urlpatterns = [
    # /signup/
    url(r'^$', views.index, name="index"),

    # /signup/confirm/<conf_link>/
    url(r'^confirm/(?P<conf_link>\d+)$', views.confirm, name='confirm'),
]