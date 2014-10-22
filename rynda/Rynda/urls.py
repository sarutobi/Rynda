# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

from rynda.core.views import NewMessagesFeed
from rynda.users.views import CreateUser

admin.autodiscover()

# Include external apps views
urlpatterns = patterns('',
    url(r'', include('social.apps.django_app.urls', namespace="social")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)

urlpatterns += patterns('core.views',
    url(r'^feed/$', NewMessagesFeed(), name="feed-new-messages"),
)

# Rynda-related patterns
urlpatterns += patterns('',
    url(r'^$', 'rynda.message.views.list', name='main-index'),
    url(r'^api/', include('rynda.api.urls')),
    url(r'^message/', include('rynda.message.urls')),
    url(r'^user/', include('rynda.users.urls')),
    url(r'^news/', include('rynda.newsline.urls')),
    url(r'^t/(?P<slug>[a-z_0-9-]+)$', 'rynda.message.views.list'),
    # url(r'^t/(?P<slug>)message/', include('message.urls')),
)

# Project description patterns
urlpatterns += patterns(
    '',
    url(r'^info/$', 'rynda.core.views.infopages', name="infopages"),
    url(r'^(?P<url>.*)/$', 'django.contrib.flatpages.views.flatpage', ),
)

# Account-related patterns
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^register$', CreateUser.as_view(), name='user-creation'),
    url(r'^login$', 'login',
        {'template_name': 'login.html'}, name='user-login'),
    url(r'^logout$', 'logout', name='user-logout'),
    url(r'^password/reset$', 'password_reset', name='user-password-reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm', name='user-password-reset-confirm'),
    url(r'^password/reset/complete$',
        'password_reset_complete', name='password_reset_complete'),
    url(r'^password/reset/done', 'password_reset_done', name="password_reset_done"),
)
