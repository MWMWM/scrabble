from django.conf.urls import patterns, url

urlpatterns = patterns('', 
url('^$', 'helper.views.ShowForm', name='form'), 
url('^SjpResult/(?P<word>\w+)$', 'helper.views.SjpResult'), 
url('^DbResult/(?P<word>\w+)$', 'helper.views.DbResult'),
url('^MyResult/(\w+)$', 'helper.views.MyResult'),
url('^Delete/(?P<word>\w+)$', 'helper.views.Delete'),
)
