from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}),
        url(r'^admin/', include(admin.site.urls)),
        )

urlpatterns += patterns('scrabble.views',
        url(r'^$', 'Home', name='home'),
        url(r'^Lang/(?P<lang>\w\w)$', 'ChangeLang', name='change_lang'),
        )

urlpatterns += patterns('log.views',
        url(r'^Login(?P<where>.+)', 'Login', name='login'),
        url(r'^Logout(?P<where>.+)', 'Logout', name='logout'),
        url(r'^Register(?P<where>.+)', 'Register', name='register'),
        url(r'^AccountSettings/(?P<username>[\w\d]+)', 'AccountSettings',
            name='account_settings'),
        )

urlpatterns += patterns('helper.views',
        url(r'^find/$', 'FindPage', name='find'),
        url(r'^add/$', 'AddPage', name='add'),
        url(r'^add/(?P<word>\w+)(?P<where>.+)$', 'AddWord',
            name='add_word'),
        url(r'^delete/(?P<word>\w+)/(?P<where>.+)$', 'Delete',
            name='delete_word'),
        )

urlpatterns += patterns('play.views',
        url(r'^start_play/$', 'StartPlay', name='start_play'),
        url(r'^play/$', 'Play', name='play'),
        url(r'letter_plus/(?P<letter>\w)$', 'AddLetter', name='letter_plus'),
        url(r'letter_minus/(?P<letter>\w)$', 'DeleteLetter', name='letter_minus'),
        url(r'^changeletters/$', 'ChangeLetters', name='changeletters'),
        url(r'^guess/$', 'Guess', name='guess'),
        url(r'^guess/(?P<result>\d+)/(?P<guesses>\d+)/(?P<all_letters>\w+)/$',
            'Guess', name='guessed'),
        url(r'^guess/(?P<result>\d+)/(?P<guesses>\d+)/(?P<all_letters>\w+)/(?P<temp_letters>\w+)$',
            'Guess', name='check_guess'),
        url(r'^(?P<where>.+)/(?P<temp_letters>\w+)/(?P<letter>\w)$',
            'Delete', name='delete_letter'),
        )
