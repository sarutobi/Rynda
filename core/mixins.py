# -*- coding: utf-8 -*-

from core.context_processors import subdomains_context, categories_context


class SubdomainContextMixin(object):
    '''Subdomain context mixin'''

    def get_context_data(self, **kwargs):
        print ('!!!')
        context = super(SubdomainContextMixin, self).get_context_data(**kwargs)
        sc = subdomains_context(self.request)
        for key in sc.keys():
            context[key] = sc[key]
        return context

