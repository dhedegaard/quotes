from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^rest/random', 'quotes.rest.rest_random'),
    url(r'^rest/latest', 'quotes.rest.rest_latest'),
    url(r'^random', 'quotes.views.random'),
    url(r'^page/([1-9]\d*)/', 'quotes.views.index'),
    url(r'', 'quotes.views.index'),
)
