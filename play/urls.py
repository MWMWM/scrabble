from django.conf.urls import patterns, url
from play import views

urlpatterns = patterns('play.views', 
url(r'^$', 'Main', {'letters': views.NewLetter()}, name = 'main'),
url(r'^(?P<result>\d+)$', 'Main', {'letters': views.NewLetter()}, name = 'main2'),
url(r'^(?P<result>\d+)\(?P<letters>(\w+)$', 'Main', name = 'main3'),
url(r'^NewLetters$', 'NewLetters', name = 'newletters'),
)
