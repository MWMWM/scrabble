from django.conf.urls import patterns, url

urlpatterns = patterns('helper.views', 
url(r'^$', 'Main', name = 'main'), 
url(r'^DbResult/(?P<word>[.\w]+)$', 'DbResult', name = 'dbresult'),
url(r'^MyResult/(?P<word>[.\w]+)$', 'MyResult', name = 'myresult'),
url(r'^(?P<xxresult>[a-zA-Z][a-zA-Z]Result)/(?P<words>[.\w]+)/(?P<word>\w+)$', 'Delete', name = 'delete'),
url(r'Login/', 'Login', name = 'login'),
url(r'Logout$', 'Logout', name = 'logout'),
)
