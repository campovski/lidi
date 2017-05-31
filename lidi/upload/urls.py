from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from . import views

app_name = 'upload'

urlpatterns = [
    # /upload/
    url(r'^$', views.upload_file, name="upload"),
]
