from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'statistics'

urlpatterns = [
    # /statistics/
    url(r'^$', views.index, name="index"),
]
