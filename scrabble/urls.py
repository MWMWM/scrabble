from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        )

urlpatterns += patterns('scrabble.views',
        url(r'^$', 'Home', name='home'),
        url(r'^Lang/(?P<lang>\w\w)$', 'ChangeLang', name='change_lang'),
        )

urlpatterns += patterns('log.views',
        url(r'^Login(?P<where>.+)', 'Login', name='login'),
        url(r'^Logout$', 'Logout', name='logout'),
        url(r'^Register(?P<where>.+)', 'Register', name='register'),
        url(r'^AccountSettings$', 'AccountSettings', name='account_settings'),
        url(r'DeleteAccount$', 'DeleteAccount', name='delete_account'),
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
        url(r'^check/$', 'Check', name='check'),
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

urlpatterns += staticfiles_urlpatterns()
