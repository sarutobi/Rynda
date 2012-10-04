#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('users.views.ajax',
    (r'^ajax$', 'list'),
    (r'^ajax/list$', 'list'),
)

urlpatterns += patterns('users.views.main',
    url(r'^list', 'list', name='users_list'),
)
