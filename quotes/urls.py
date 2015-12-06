from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

from . import views, rest

urlpatterns = patterns('',
    url(r'^rest/random/$', rest.rest_random, name='rest_random'),
    url(r'^rest/latest/$', rest.rest_latest, name='rest_latest'),
    url(r'^random/$', views.random, name='random'),
    url(r'^$', views.index, name='index'),
)
