# -*- coding: utf-8 -*-
#Core context processors for Rynda project

from operator import itemgetter
from core.models import Subdomain


def subdomains_context(request):
    '''Create a subdomains context lists'''
    subdomains = list(Subdomain.objects.values('id', 'url', 'title', 'isCurrent').filter(status=1))
    visible_subs = subdomains[:5]
    hidden_subs = subdomains[5:14]
    domain = request.META['HTTP_HOST'].split('.')
    if len(domain) == 3:
        current_sub = domain[0]
        base_url = "%s.%s" % (domain[1], domain[2])
    else:
        current_sub = ''
        base_url = "%s.%s" % (domain[0], domain[1])
    return {
        'visible_subs': visible_subs,
        'hidden_subs': hidden_subs,
        'current_sub': current_sub,
        'base_url': base_url,
    }
