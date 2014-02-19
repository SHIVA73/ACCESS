'''
Created on Oct 26, 2012

@author: god
'''
from django.contrib import admin
from django.conf.urls import patterns, url, include
admin.autodiscover()
from django.conf import settings


urlpatterns = patterns('uam.views',
    url(r'^/$', 'login'),
    url(r'^login/$', 'login'),
#    url(r'^mymedia/(?P<path>.*)$', 'serve',
#        {'document_root': settings.MEDIA_ROOT,}),
#    url(r'^mystatic/(?P<path>.*)$', 'static.serve',
#            {'document_root':     settings.STATIC_ROOT}),
    url(r'^setting/$','setting'),
    url(r'^config/$','config'),
    url(r'^authent/$','authent'), # authentication
    url(r'^daily/$','daily'),
    url(r'^home/$','home'),
    # url(r'^admin/$', include(admin.site.urls)),
    url(r'^logout_view/$','logout_view'),
    
    # url(r'^$', 'form', name='form'), 
    # url(r'^find_cities/$', 'find_cities', name='find_cities'),
    
    
    
    
    
)
urlpatterns += patterns('django.views.static',
        (r'mymedia/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
