from django.conf.urls import url

from . import views

app_name = 'statistics'

urlpatterns = [
    # /statistics/
    url(r'^$', views.index, name='index'),

    # /statistics/problem/
    url(r'^problem/$', views.problem, name='problem'),

    # /statistics/problem/<problem_id>/
    url(r'^problem/(?P<problem_id>\d+)/$', views.problem, name='problem_detail'),

    # /statistics/country/
    url(r'^country/$', views.country, name='country'),

    # /statistics/country/<country_slug>/
    url(r'^country/(?P<country_slug>[a-z_]+)/$', views.country, name='country_detail'),

    # /statistics/users/
    url(r'^users/$', views.users, name='users'),

    # /statistics/users/<username>
    url(r'^users/(?P<username>[0-9a-zA-Z_]+)/$', views.users, name='users_detail'),

    # /statistics/achievements/
    url(r'^achievements/$', views.achievements, name='achievements'),

    # /statistics/achievements/<achievement_id>/
    url(r'^achievements/(?P<achievement_id>\d+)/$', views.achievements, name='achievements_detail')
]
