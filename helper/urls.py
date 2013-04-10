from django.conf.urls import patterns, url

urlpatterns = patterns('helper.views', 
url(r'^$', 'Main', name = 'h_main'), 
url(r'^(?P<xx>[a-zA-z]+)Result/(?P<word>[*\w]+)$', 'XxResult', name = 'xxresult'),
url(r'^(?P<xxresult>[a-zA-Z][a-zA-Z]Result)/(?P<words>[*\w]+)/(?P<word>\w+)$', 'Delete', name = 'delete'),
)
