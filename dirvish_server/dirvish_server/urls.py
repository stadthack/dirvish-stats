from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dirvishserver.views.index'),
    url(r'^index.*', 'dirvishserver.views.index'),
    url(r'^hosts.*', 'dirvishserver.views.hosts'),
    url(r'^trend.*', 'dirvishserver.views.trend'),
    url(r'^top.*', 'dirvishserver.views.topx'),
    url(r'^detail.*', 'dirvishserver.views.detail'),

    # url(r'^dirvish_server/', include('dirvish_server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
