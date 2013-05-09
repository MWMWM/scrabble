from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from play.views import NewLetters
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}),
        url(r'^admin/', include(admin.site.urls)),
        )

urlpatterns += patterns('scrabble.views',
        url (r'^$', 'Home', name='home'),
        url(r'^Pl(?P<where>.+)$', 'ChangeLang', {'lang': 'pl'}, 
            name='lang_pl'),
        url(r'^En(?P<where>.+)$', 'ChangeLang', {'lang': 'en'},
            name='lang_en'),
        )

urlpatterns += patterns('log.views',
        url(r'^Login(?P<where>.+)', 'Login', name='login'),
        url(r'^Logout(?P<where>.+)', 'Logout', name='logout'),
        url(r'^Register(?P<where>.+)', 'Register', name='register'),
        )

urlpatterns += patterns('helper.views', 
        url(r'^find/$', 'FindPage', name = 'find'),
        url(r'^add/$', 'AddPage', name = 'add'),
        url(r'^add/(?P<word>\w+)(?P<where>.+)$', 'AddWord', 
            name='add_word'),
        url(r'^find/(?P<words>[*\w]+)/(?P<word>\w+)$', 'Delete', 
            name = 'delete_word'),
        )

urlpatterns += patterns('play.views', 
        url(r'^play/$', 'Main', name = 'play'),
        url(r'^play/(?P<result>\d+)/(?P<all_letters>\w+)/(?P<temp_letters>\w*)$', 
            'Playing', name = 'playing'),
        url(r'^changeletters/(?P<result>\d+)(?P<letters>\w+)$', 'ChangeLetters', 
            name = 'changeletters'),
        )
