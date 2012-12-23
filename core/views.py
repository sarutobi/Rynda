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
