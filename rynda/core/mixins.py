# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView


class PaginatorMixin(object):
    """ Paginator line mixin. Best use with list-based mixins """

    def paginator(self, num_pages, page=1, adj_pages=2, outside_range=3):
        page = int(page)
        num_pages = int(num_pages)
        if page > num_pages:
            page = num_pages

        if page < 1:
            page = 1
        has_prev = has_next = False
        if num_pages > 1:
            if page > 1:
                has_prev = True
            if page < num_pages:
                has_next = True
        # Counts minimal pages to work
        pager_size = 2 * (outside_range + adj_pages) + 1

        # If pager_size greater than total pages - pager wil show all pages in
        # range
        if pager_size >= num_pages:
            return {
                'first': [], 'window': [n for n in range(1, num_pages + 1)],
                'last': [],  'has_prev': has_prev, 'has_next': has_next}

        # Checking page windows
        # Current page in first (low) window
        if (outside_range + adj_pages + 1) >= page:
            first = []
            window = [n for n in range(
                1, outside_range + 2 + 2 * adj_pages)
                if n > 0 and n < num_pages]
            last = [n for n in range(num_pages - outside_range, num_pages+1)]
        # Current page in middle window
        elif (num_pages - outside_range - adj_pages - 1) < page:
            first = [n for n in range(1, outside_range + 1)]
            window = [n for n in range(
                num_pages - outside_range - 2 * adj_pages + 1, num_pages + 1)]
            last = []
        # Current page in last (high) window
        else:
            first = [n for n in range(1, outside_range + 1)]
            last = [n for n in range(
                num_pages - outside_range + 1, num_pages+1)]
            window = [n for n in range(
                page - adj_pages, page + adj_pages + 1)
                if n < num_pages]
        return {
            'first': first, 'window': window, 'last': last,
            'has_prev': has_prev, 'has_next': has_next}


class QueryStringMixin(object):
    """ This mixin adds a query string to context. """

    def get_context_data(self, **kwargs):
        context = super(QueryStringMixin, self).get_context_data(**kwargs)
        context['query_string'] = u'?%s' % self.request.META['QUERY_STRING']
        return context
