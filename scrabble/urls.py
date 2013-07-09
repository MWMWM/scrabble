from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^captcha/', include('captcha.urls')),
        url(r'^accounts/login/', 'log.views.Login'),
        )

urlpatterns += patterns('scrabble.views',
        url(r'^$', 'Home', name='home'),
        url(r'^Lang/(?P<lang>\w+)/(?P<where>.+)$', 'ChangeLang',
            name='change_lang'),
        )

urlpatterns += patterns('log.views',
        url(r'^Login(?P<where>.+)', 'Login', name='login'),
        url(r'^Logout$', 'Logout', name='logout'),
        url(r'^Register(?P<where>.+)', 'Register', name='register'),
        url(r'^AccountSettings$', 'AccountSettings', name='account_settings'),
        url(r'DeleteAccount$', 'DeleteAccount', name='delete_account'),
        url(r'CheckAvailability/$', 'CheckAvailability', name='check_availability'),
        )

urlpatterns += patterns('helper.views',
        url(r'^find/$', 'FindPage', name='find'),
        url(r'^add/$', 'AddPage', name='add'),
        url(r'^add/(?P<word>\w+)(?P<where>.+)$', 'AddWord',
            name='add_word'),
        url(r'^delete/(?P<word>\w+)/(?P<where>.+)$', 'Delete',
            name='delete_word'),
        url(r'^add_lang/(?P<where>.+)$', 'AddLanguage', name='add_lang'),
        )

urlpatterns += patterns('play.views',
        url(r'^start_play/$', 'StartPlay', name='start_play'),
        url(r'^play_/$', 'Play', name='play'),
        url(r'^check/$', 'Check', name='check'),
        url(r'letter_plus/(?P<letter>\w)$', 'AddLetter', name='letter_plus'),
        url(r'letter_minus/(?P<letter>\w)$', 'DeleteLetter', name='letter_minus'),
        url(r'^changeletters/$', 'ChangeLetters', name='changeletters'),
        url(r'^guess/$', 'Guess', name='guess'),
        url(r'^check_guess/$', 'CheckGuess', name='check_guess'),
        )

urlpatterns += staticfiles_urlpatterns()
