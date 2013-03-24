from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'$', 'scrabble.views.Main'),
    url(r'^help/', include('helper.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'helper.views.Login'),
    #url(r'^accounts/login/$', 'helper.views.Login'),
    # url(r'^scrabble/', include('scrabble.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
