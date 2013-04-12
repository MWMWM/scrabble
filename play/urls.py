from django.conf.urls import patterns, url

urlpatterns = patterns('play.views', 
url(r'^$', 'Main', name = 'p_main'),
url(r'^NewLetters$', 'NewLetters', name = 'newletters'),
url(r'^create$', 'Create', name='click2'),
)
