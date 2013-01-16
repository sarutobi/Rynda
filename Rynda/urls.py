# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from users.views import CreateUser

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RyndaRebuild.views.home', name='home'),
    # url(r'^RyndaRebuild/', include('RyndaRebuild.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'message.views.list'),
    url(r'^t/(?P<slug>[a-z_0-9-]+)$', 'message.views.list'),
    url(r'^register$', CreateUser.as_view()),
    url(r'^login$', 'django.contrib.auth.views.login',\
        {'template_name': 'login.html'}),
    url(r'^logout$', 'message.views.logout_view'),
    url(r'^message/', include('message.urls')),
    url(r'^t/(?P<slug>)message/', include('message.urls')),
    url(r'^user/', include('users.urls')),
    ('^info/(?P<slug>[a-z_]+)$', 'core.views.show_page'),
)

urlpatterns += patterns('core.views',

)

urlpatterns += patterns('',
    (r'^api/', include('api.urls')),
)
