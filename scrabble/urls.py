from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from play.views import NewLetters
admin.autodiscover()

urlpatterns = patterns('',
    url(r'media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
  )

urlpatterns += patterns('log.views',
        url(r'^Login(?P<where>.+)', 'Login', name='login'),
        url(r'^Logout(?P<where>.+)', 'Logout', name='logout'),
        url(r'^Register(?P<where>.+)', 'Register', name='register'),
)

urlpatterns += patterns('helper.views', 
        url(r'^find/$', 'FindPage', name = 'find'),
        url(r'^add/$', 'AddPage', name = 'add'),
        url(r'^add/(?P<word>\w+)(?P<where>[/\w]+)$', 'AddWord', 
            name='add_word'),
        url(r'^find/(?P<where>[a-zA-Z]+)/(?P<word>[*\w]+)$', 'XxResult', 
            name = 'xxresult'),
        url(r'^delete/(?P<where>[a-zA-Z]+Result/[*\w]+)/(?P<word>\w+)$', 
            'Delete', name = 'delete_word'),
        )

urlpatterns += patterns('play.views', 
        url(r'^play/$', 'Playing', {'letters': NewLetters()}, name = 'play'),
        url(r'^play/(?P<result>\d+)/(?P<letters>\w+)$', 'Playing', 
            name = 'playing'),
        url(r'^changeletters/(?P<result>\d+)(?P<letters>\w+)$', 'ChangeLetters', 
            name = 'changeletters'),
        )
