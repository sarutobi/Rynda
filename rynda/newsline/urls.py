# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from .views import NewsListView

urlpatterns = patterns(
    '',
    url(r'^$', NewsListView.as_view(), name='news-list-view'),
)

