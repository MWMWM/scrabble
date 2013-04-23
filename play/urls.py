from django.conf.urls import patterns, url
from play import views

urlpatterns = patterns('play.views', 
        url(r'^$', 'Main', name = 'main'),
        url(r'^(?P<result>\d+)/(?P<letters>\w+)$', 'Playing', name = 'playing'),
        url(r'^NewLetters/(?P<result>\d+)$', 'NewLetters', name = 'newletters'),
        )
