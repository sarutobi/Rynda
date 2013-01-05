#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from users.views import UserDetail, UserList


urlpatterns = patterns('users.views.ajax',
    url(r'^$', UserList.as_view()),
    url(r'^page/(?P<page>\d+)$', UserList.as_view()),
    url(r'^(?P<pk>\d+)$', UserDetail.as_view()),
#    (r'^ajax$', 'list'),
#    (r'^ajax/list$', 'list'),
)

#urlpatterns += patterns('users.views.main',
#    url(r'^list', 'list', name='users_list'),
#)
