#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from users.views import UserDetail, UserList, ForgotPassword


urlpatterns = patterns('users.views',
    url(r'^$', UserList.as_view()),
    url(r'^page/(?P<page>\d+)$', UserList.as_view()),
    url(r'^(?P<pk>\d+)$', UserDetail.as_view()),
    url(r'^activate/(?P<pk>\d+)/(?P<key>[a-f0-9]{40})$', 'activate_profile'),
    url(r'^forgotpassword$', ForgotPassword.as_view()),
    #url(r'^requestpassword$', ''),
    #url(r'^resetpassword/(?P<key>[a-f0-9]{40})$', ''),
)

