from django.conf.urls import patterns, url

urlpatterns = patterns('helper.views', 
url(r'^$', 'Main', name = 'main'), 
url(r'^DbResult/(?P<word>[.\w]+)$', 'DbResult', name = 'dbresult'),
url(r'^MyResult/(?P<word>[.\w]+)$', 'MyResult', name = 'myresult'),
url(r'^[a-zA-Z][a-zA-Z]Result/(?P<prev>[.\w]+)/Delete/(?P<word>\w+)$', 'Delete', name = 'delete'),
url(r'^AddWord/(.+)$', 'AddWord', name = 'addword'),
url(r'AddWords$', 'AddWords', name = 'addwords'),
url(r'Login/', 'Login', name = 'login'),
url(r'Logout$', 'Logout', name = 'logout'),
)
