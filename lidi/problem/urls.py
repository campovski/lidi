from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'problem'

urlpatterns = [
    # /problems/
    url(r'^$', views.index, name="index"),

    # /problems?page=<page>?sort=<sort_by>/
    url(r'^\\?page=(?P<page>[0-9]+)\\?sort=(?P<sort_by>[\s\S]+)/$', views.index, name="index"),

    # /problems/<problem_id>/
    url(r'^(?P<problem_id>[0-9]+)/$', views.detail, name="detail"),
]
