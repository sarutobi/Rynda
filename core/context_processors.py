# -*- coding: utf-8 -*-
#Core context processors for Rynda project

from django.conf import settings

from category.models import Category, CategoryGroup


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
