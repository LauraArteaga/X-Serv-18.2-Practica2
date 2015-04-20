from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', "acorta.views.getForm"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(.*)$', "acorta.views.getUrl"),
)
