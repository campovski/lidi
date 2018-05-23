from django.conf.urls import url

from . import views

app_name = 'upload'

urlpatterns = [
    # /upload/
    url(r'^$', views.upload_file, name="upload"),
]
