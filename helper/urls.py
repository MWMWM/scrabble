from django.conf.urls import patterns, url

urlpatterns = patterns('helper.views', 
        url(r'^$', 'Main', name = 'main'), 
        url(r'^(?P<xx>[a-zA-z]+)Result/(?P<word>[*\w]+)$', 'XxResult', name = 'xxresult'),
        url(r'^(?P<where>[a-zA-Z]+Result/[*\w]+)/(?P<word>\w+)$', 'Delete', name = 'delete'),
        )
