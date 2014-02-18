# -*- coding: utf-8 -*-
#Core context processors for Rynda project

from django.conf import settings

from category.models import Category, CategoryGroup

from .models import Subdomain


def subdomains_context(request):
    """ Create a subdomains context lists. """
    subdomains = list(
        Subdomain.objects
        .values('id', 'url', 'title', 'isCurrent')
        .filter(status=1))
    visible_subs = subdomains[:5]
    hidden_subs = subdomains[5:14]
    domain = request.META['HTTP_HOST'].split('.', 1)
    if len(domain) == 2:
        current_sub = domain[0]
        base_url = domain[1]
    else:
        current_sub = ''
        base_url = domain[0]
    return {
        'visible_subs': visible_subs,
        'hidden_subs': hidden_subs,
        'current_sub': current_sub,
        'base_url': base_url,
    }


def categories_context(request):
    """ Categories hierarchy. """
    cats = CategoryGroup.objects.values('id', 'name').all()
    tree = [c for c in cats]
    for l in tree:
        l['children'] = [c for c in Category.objects.values(
            'id', 'name').filter(group=l['id'])]
    return {'categories': tree, }


def production_context(request):
    """ Add production mode flag. """
    return {'production': settings.PRODUCTION, }
