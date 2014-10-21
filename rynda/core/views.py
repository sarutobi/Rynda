# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView

from core.mixins import PaginatorMixin, QueryStringMixin

from message.models import Message


class NewMessagesFeed(Feed):
    title = _("Latest messages")
    description = _("Latest messages")
    link = reverse_lazy("messages-list")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.message

    def items(self):
        return Message.objects.active().all()[:10]


class RyndaListView(QueryStringMixin, PaginatorMixin, ListView):
    paginator_url = None
    list_title_short = None

    def get_paginator_url(self):
        if self.paginator_url is None:
            raise Exception(
               "You MUST define paginator_url or overwrite get_paginator_url()")
        return self.paginator_url

    def get_context_data(self, **kwargs):
        context = super(RyndaListView, self).get_context_data(**kwargs)
        context['paginator_url'] = self.get_paginator_url()
        sc = self.paginator(
            context['paginator'].num_pages,
            page=context['page_obj'].number)
        context['paginator_line'] = sc
        context['listTitleShort'] = self.list_title_short
        return context


def infopages(request):
    return render(
        request,
        'infopages_list.html',)
