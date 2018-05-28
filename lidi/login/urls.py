from django.conf.urls import url

from . import views

app_name = 'login'

urlpatterns = [
    # /login/
    url(r'^$', views.index, name="index"),

    # /login/out/
    url(r'^out/$', views.logout, name="logout"),

    # /login/reset_password/<conf_link>/
    url(r'^reset_password/(?P<conf_link>\d+)$', views.reset_password, name='reset_password'),

    # /login/reset_password/
    url(r'^reset_password/$', views.reset_password, name='reset_password')
]
