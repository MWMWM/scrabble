from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^Login(?P<where>.+)', 'scrabble.views.Login', name='login'),
    url(r'^Logout(?P<where>.+)', 'scrabble.views.Logout', name='logout'),
    url(r'^help/', include('helper.urls')),
    url(r'^play/', include('play.urls')),
    url(r'^admin/', include(admin.site.urls)),
  )
