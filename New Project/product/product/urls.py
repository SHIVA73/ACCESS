from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
# from product.UAM import urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'uam.views.login'),
    # url(r'^product/', include('product.foo.urls')),
    url(r'^uam/', include('uam.urls')),
    url(r'^AccessCore/', include('accesscore.urls')),
    url(r'^AccessCore/', include('leaveapp.urls')),
    url(r'^LeaveApp/', include('leaveapp.urls')),
    # url(r'^AccessCore/Forms/Add_Company/', include('AccessCore.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.static',
        (r'mymedia/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
