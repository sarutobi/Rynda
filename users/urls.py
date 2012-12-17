#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from users.views import UserDetail


urlpatterns = patterns('users.views.ajax',
    (r'^(?P<pk>\d+)$', UserDetail.as_view()),
#    (r'^ajax$', 'list'),
#    (r'^ajax/list$', 'list'),
)

#urlpatterns += patterns('users.views.main',
#    url(r'^list', 'list', name='users_list'),
#)
