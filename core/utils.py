# -*- coding: utf-8 -*-

from core.models import Subdomain

def url_filter(queryset, slug):
    '''
    Filtering external message queryset according
    to requested theme.
    '''
    t = Subdomain.objects.filter(slug=slug).count()
    if t == 1:
        return queryset.filter(subdomain__url=slug)
    return queryset
