# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from core.mixins import SubdomainContextMixin


class RyndaCreateView(SubdomainContextMixin, CreateView):
    pass

class RyndaDetailView(SubdomainContextMixin, DetailView):
    pass
