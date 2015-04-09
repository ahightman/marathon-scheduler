from django.conf.urls import patterns, include, url
from django.contrib import admin
from schedule.views import schedule, date

urlpatterns = patterns('',
    # Examples:
    url(r'^schedule/$', schedule),
    url(r'^date/$', date),
    url(r'^admin/', include(admin.site.urls))
)
