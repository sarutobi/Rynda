# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from core.mixins import SubdomainContextMixin, PaginatorMixin


class RyndaCreateView(SubdomainContextMixin, CreateView):
    pass


class RyndaDetailView(SubdomainContextMixin, DetailView):
    pass


class RyndaListView(SubdomainContextMixin, PaginatorMixin, ListView ):
    pass


def show_page(request, slug):
    page = get_object_or_404(Infopage, slug=slug)
    return render_to_response('infopage/show_page.html',
        {'title': page.title, 'text': page.text, },
        context_instance=RequestContext(request,
            processors=[subdomains_context, categories_context])
    )

