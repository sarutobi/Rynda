# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from api.views import MessagesList, CategoryList, CategoryDetail,\
    MapMessageList

urlpatterns = patterns('api.views',
    url(r'^$', 'api_root'),
    url(r'^messages/$', MessagesList.as_view(), name='messages-list'),
    url(r'^categories/$', CategoryList.as_view(), name='cat-list'),
    url(r'^categories/(?P<pk>\d+)/$', CategoryDetail.as_view(),
        name='category-detail'),
    url(r'^internal/mapmessages/$', MapMessageList.as_view()),
)


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
