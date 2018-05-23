from django.conf.urls import url
from . import views


app_name = 'home'

urlpatterns = [
    # /problems/
    url(r'^$', views.index, name="index"),
]
