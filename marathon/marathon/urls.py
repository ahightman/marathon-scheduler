from django.conf.urls import patterns, include, url
from django.contrib import admin

from schedule.views import index

urlpatterns = patterns('',
    # Examples:
    url(r'^index/$', index),
    url(r'^admin/', include(admin.site.urls)),
)
