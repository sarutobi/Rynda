# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from core.mixins import (
    PaginatorMixin, QueryStringMixin, ExternalScriptsMixin)


class RyndaCreateView(CreateView):
    pass


class RyndaDetailView(ExternalScriptsMixin, DetailView):
    pass


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


class RyndaFormView(FormView):
    pass


def infopages(request):
    return render(
        request,
        'infopages_list.html',)
