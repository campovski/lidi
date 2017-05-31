from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from . import views

app_name = 'login'

urlpatterns = [
    # /login/
    url(r'^$', views.index, name="index"),

    # /login/out/
    url(r'^out/$', views.logout, name="logout")
]
