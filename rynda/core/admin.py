# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site

from .models import SocialLinkType, SiteSocialLinks


class SocialLinkInline(admin.StackedInline):
    model = SiteSocialLinks


class MySiteAdmin(SiteAdmin):
    inlines = [SocialLinkInline, ]


class SocialLinkTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')

admin.site.register(SocialLinkType, SocialLinkTypeAdmin)
admin.site.unregister(Site)
admin.site.register(Site, MySiteAdmin)
