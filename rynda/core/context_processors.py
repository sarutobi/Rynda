# -*- coding: utf-8 -*-
# Core context processors for Rynda project

from django.conf import settings
from django.contrib.sites.models import Site


def production_context(request):
    """ Add production mode flag. """
    return {'production': settings.PRODUCTION, }


def current_site(request):
    """ Append a site context object to templates """

    site = Site.objects.get_current()
    contacts = site.sitesociallinks_set.prefetch_related().all()
    return {'current_site': site, 'contacts': contacts, }
