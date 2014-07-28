# -*- coding: utf-8 -*-
#Core context processors for Rynda project

from django.conf import settings


def production_context(request):
    """ Add production mode flag. """
    return {'production': settings.PRODUCTION, }
