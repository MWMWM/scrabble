from django.conf.urls import patterns, url
from play import views

urlpatterns = patterns('play.views', 
        url(r'^$', 'Playing', {'letters': views.NewLetters()}, name = 'main'),
        url(r'^(?P<result>\d+)/(?P<letters>\w+)$', 'Playing', name = 'playing'),
        url(r'^ChangeLetters/(?P<result>\d+)$', 'ChangeLetters', name = 'changeletters'),
        )
