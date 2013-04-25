from django.conf.urls import patterns, url

urlpatterns = patterns('helper.views', 
        url(r'^$', 'Main', name = 'main'),
        url(r'^Add/(?P<word>\w+)(?P<where_next>[/\w]+)$', 'AddWord', name='add_word'),
        url(r'^(?P<where>[a-zA-z]+)/(?P<word>[*\w]+)$', 'XxResult', name = 'xxresult'),
        url(r'^(?P<where>[a-zA-Z]+Result/[*\w]+)/(?P<word>\w+)$', 'Delete', name = 'delete'),
        )
