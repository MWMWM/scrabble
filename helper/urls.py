from django.conf.urls import patterns, url

urlpatterns = patterns('', 
url('^$', 'helper.views.ShowForm', name='form'), 
url('^SjpResult/(?P<word>\\w+)$', 'helper.views.SjpResult'), 
url('^DbResult/(?P<word>\\w+)$', 'helper.views.DbResult'), 
url('^AddOne/(?P<word>\\w+)$', 'helper.views.AddOne'), 
url('^AddMultiple', 'helper.views.AddMultiple'))

