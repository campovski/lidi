from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

app_name = 'lidi'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', include('login.urls')),
    url(r'^problems/', include('problem.urls')),
    url(r'^upload/', include('upload.urls')),
    url(r'^signup/', include('signup.urls')),
    url(r'^statistics/', include('statistics.urls')),
    url(r'^', include('home.urls')),
]
