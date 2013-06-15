# -*- coding: utf-8 -*-

from django.conf import settings

from core.context_processors import subdomains_context, categories_context
from core.models import Category, CategoryGroup


class SubdomainContextMixin(object):
    '''Subdomain context mixin'''

    def get_context_data(self, **kwargs):
        context = super(SubdomainContextMixin, self).get_context_data(**kwargs)
        sc = subdomains_context(self.request)
        for key in sc.keys():
            context[key] = sc[key]
        return context


class PaginatorMixin(object):
    '''Paginator line mixin. Best use with list-based mixins'''

    def paginator(self, num_pages, page = 1, adj_pages = 2, outside_range = 3):
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
        #Количество страниц для отображения меньше чем количество 
        #страниц в пейджере
        if (outside_range + adj_pages + 1 + adj_pages + outside_range)\
            >= num_pages:
            return {'first':[],'window':[n for n in range(1, num_pages+1)],
                'last':[],  'has_prev':has_prev, 'has_next':has_next}

        #страница для отображения находится в начальном диапазоне
        if (outside_range + adj_pages + 1 ) >= page:
            first = []
            window = [n for n in range(1, outside_range + 2 + 2 * adj_pages)
                if n > 0 and n < num_pages]
            last = [n for n in range(num_pages - outside_range, num_pages+1)]
        elif (num_pages - outside_range - adj_pages - 1) < page:
            first = [n for n in range(1, outside_range + 1)]
            window = [n for n in range(num_pages - outside_range - 2 *
                adj_pages + 1, num_pages +1)]
            last = []
        else:
            first = [n for n in range(1, outside_range + 1)]
            last = [n for n in range(num_pages - outside_range + 1,
                num_pages+1)]
            window = [n for n in range(page - adj_pages, page + adj_pages +1)
                if n < num_pages]
        return {'first':first, 'window':window, 'last':last,
            'has_prev':has_prev, 'has_next':has_next}


class CategoryMixin(object):
    '''Category mixin'''
    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        cats = CategoryGroup.objects.values('id', 'name').all()
        tree = [c for c in cats]
        for l in tree:
            l['children'] = [c for c in Category.objects.values(
                'id', 'name').filter(group=l['id'])]
        context['categories'] = tree
        return context


class ExternalScriptsMixin(object):

    def allow_external(self):
        return settings.EXTERNAL
