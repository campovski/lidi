from django.conf.urls import url

from . import views

app_name = 'signup'

urlpatterns = [
    # /signup/
    url(r'^$', views.index, name="index"),

    # /signup/confirm/<conf_link>/
    url(r'^confirm/(?P<conf_link>\d+)$', views.confirm, name='confirm'),
]
