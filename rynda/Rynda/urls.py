# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages import views as flatpage_view
from django.contrib.auth import views as auth_views

from rynda.core import views as core_views
from rynda.core.views import NewMessagesFeed
#  from rynda.users.views import CreateUser

from rynda.message import views as message_views

admin.autodiscover()

# Include external apps views
urlpatterns = [
    #  url(r'', include('social.apps.django_app.urls', namespace="social")),
    url(r'^admin/', admin.site.urls),
    url(r'^grappelli/', include('grappelli.urls')),
]

urlpatterns += [
    url(r'^feed/$', NewMessagesFeed(), name="feed-new-messages"),
]

# Rynda-related patterns
urlpatterns += [
    url(r'^$', message_views.list, name='main-index'),
    #  url(r'^api/', include('rynda.api.urls')),
    url(r'^message/', include('rynda.message.urls')),
    #  url(r'^user/', include('rynda.users.urls')),
    #  url(r'^news/', include('rynda.newsline.urls')),
    #  url(r'^t/(?P<slug>[a-z_0-9-]+)$', message_views.list),
    # url(r'^t/(?P<slug>)message/', include('message.urls')),
]

# Project description patterns
urlpatterns += [
    url(r'^info/$', core_views.infopages, name="infopages"),
    url(r'^(?P<url>.*)/$', flatpage_view.flatpage, ),
]

# Account-related patterns
urlpatterns += [#'django.contrib.auth.views',
    #  url(r'^register$', CreateUser.as_view(), name='user-creation'),
    #  url(r'^login$', 'login',
        #  {'template_name': 'login.html'}, name='user-login'),
    #  url(r'^logout$', 'logout', name='user-logout'),
    #  url(r'^password/reset$', 'password_reset', name='user-password-reset'),
    #  url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        #  'password_reset_confirm', name='user-password-reset-confirm'),
    #  url(r'^password/reset/complete$',
        #  'password_reset_complete', name='password_reset_complete'),
    #  url(r'^password/reset/done', 'password_reset_done', name="password_reset_done"),
]
