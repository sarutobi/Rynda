#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from users.views import UserDetail, UserList


urlpatterns = patterns('users.views',
    url(r'^$', UserList.as_view()),
    url(r'^page/(?P<page>\d+)/$', UserList.as_view()),
    url(r'^(?P<pk>\d+)$', UserDetail.as_view()),
    url(r'^activate/(?P<pk>\d+)(?P<key>[a-f0-9]{40})$', 'activate_profile'),
    #url(r'^requestpassword$', ''),
)

