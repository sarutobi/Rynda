# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site

#  from leaflet.forms.widgets import LeafletWidget

from .models import SocialLinkType, SiteSocialLinks, SiteMapOptions


class SocialLinkInline(admin.StackedInline):
    model = SiteSocialLinks


#  class SiteMapInline(admin.StackedInline):
    #  model = SiteMapOptions

    #  class Meta:
        #  widgets = {'center': LeafletWidget()}

class MySiteAdmin(SiteAdmin):
    inlines = [SocialLinkInline, ] #, SiteMapInline]


class SocialLinkTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')

admin.site.register(SocialLinkType, SocialLinkTypeAdmin)
admin.site.unregister(Site)
admin.site.register(Site, MySiteAdmin)
