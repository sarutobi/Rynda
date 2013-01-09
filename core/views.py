# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.template import RequestContext

from core.mixins import SubdomainContextMixin, PaginatorMixin
from core.models import Infopage
from core.context_processors import subdomains_context, categories_context

class RyndaCreateView(SubdomainContextMixin, CreateView):
    pass

class RyndaDetailView(SubdomainContextMixin, DetailView):
    pass

class RyndaListView(SubdomainContextMixin, PaginatorMixin, ListView ):
    paginator_url = None

    def get_paginator_url(self):
        if self.paginator_url is None:
            raise Exception(
              "You MUST define paginator_url or overwrite get_paginator_url()")
        return self.paginator_url

    def get_context_data(self, **kwargs):
        context = super(RyndaListView, self).get_context_data(**kwargs)
        context['paginator_url'] = self.get_paginator_url()
        sc = self.paginator(context['paginator'].num_pages, page=context['page_obj'].number)
        context['paginator_line'] = sc
        return context


class RyndaFormView(SubdomainContextMixin, FormView):
    pass

def show_page(request, slug):
    page = get_object_or_404(Infopage, slug=slug)
    return render_to_response('infopage/show_page.html',
        {'title': page.title, 'text': page.text, },
        context_instance=RequestContext(request,
            processors=[subdomains_context, categories_context])
    )

