#-*- coding: utf-8 -*-

from django.conf.urls import  url

from rynda.users.views import UserDetail, UserList, EditProfile, activate_profile


urlpatterns = ['rynda.users.views',
    url(r'^$', UserList.as_view(), name="user-list"),
    url(r'^page/(?P<page>\d+)/$', UserList.as_view(), name='user-list'),
    url(r'^(?P<pk>\d+)$', UserDetail.as_view(), name='user-details'),
    url(r'^activate/(?P<pk>\d+)/(?P<key>[a-zA-Z0-9_-]+)/$',
        activate_profile, name='user-activate-profile'),
    url(r'^edit/$', EditProfile.as_view(), name='user-profile-edit'),
    #url(r'^requestpassword$', ''),
]
