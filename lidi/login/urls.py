from django.conf.urls import url

from . import views

app_name = 'login'

urlpatterns = [
    # /login/
    url(r'^$', views.index, name="index"),

    # /login/out/
    url(r'^out/$', views.logout, name="logout")
]
