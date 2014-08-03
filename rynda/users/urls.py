#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from users.views import UserDetail, UserList


urlpatterns = patterns('users.views',
    url(r'^$', UserList.as_view(), name="user-list"),
    url(r'^page/(?P<page>\d+)/$', UserList.as_view(), name='user-list'),
    url(r'^(?P<pk>\d+)$', UserDetail.as_view(), name='user-details'),
    url(r'^activate/(?P<pk>\d+)(?P<key>[a-f0-9]{40})$', 'activate_profile', name='user-activate-profile'),
    #url(r'^requestpassword$', ''),
)
