from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^json/random', 'quotes.json.json_random'),
    url(r'^json/latest', 'quotes.json.json_latest'),
    url(r'^random', 'quotes.views.random'),
    url(r'^page/([1-9]\d*)/', 'quotes.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', 'quotes.views.index'),
)
