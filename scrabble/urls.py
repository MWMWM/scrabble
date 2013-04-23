from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^Login(?P<where>.+)', 'log.views.Login', name='login'),
    url(r'^Logout(?P<where>.+)', 'log.views.Logout', name='logout'),
    url(r'^help/', include('helper.urls', namespace="help")),
    url(r'^play/', include('play.urls', namespace="play")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^log/', 'django.contrib.auth.views.login'),
  )
