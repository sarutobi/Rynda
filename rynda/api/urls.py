# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import MessagesList, CategoryList, CategoryDetail,\
    MapMessageList

urlpatterns = patterns('rynda.api.views',
    url(r'^$', 'api_root'),
    url(r'^messages/$', MessagesList.as_view(), name='api-messages-list'),
    url(r'^categories/$', CategoryList.as_view(), name='api-cat-list'),
    url(r'^categories/(?P<pk>\d+)/$', CategoryDetail.as_view(),
        name='api-category-detail'),
    url(r'^internal/mapmessages/$', MapMessageList.as_view(), name="get-map-markers"),
)


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
