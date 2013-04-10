from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^Login/$', 'scrabble.views.Login', name='login'),
    url(r'^Logout/$', 'scrabble.views.Logout', name='logout'),
    url(r'^help/', include('helper.urls')),
    url(r'^play/', include('play.urls')),
    url(r'^admin/', include(admin.site.urls)),

  )
