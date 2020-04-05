# -*- coding: utf-8 -*-

from django.conf.urls import  include, url

from .views import NewsListView

urlpatterns = [
    '',
    url(r'^$', NewsListView.as_view(), name='news-list-view'),
]

