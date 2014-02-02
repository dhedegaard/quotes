from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^rest/random$', 'quotes.rest.rest_random', name='rest_random'),
    url(r'^rest/latest$', 'quotes.rest.rest_latest', name='rest_latest'),
    url(r'^random$', 'quotes.views.random', name='random'),
    url(r'^page/(\d+)/$', 'quotes.views.index', name='index_page'),
    url(r'^$', 'quotes.views.index', name='index'),
)
