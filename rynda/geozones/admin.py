# -*- coding: utf-8 -*-

from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Region, Location


class RegionAdmin(LeafletGeoAdmin):
    prepopulated_fields = {"slug": ("name", ), }


admin.site.register(Region, RegionAdmin)

admin.site.register(Location, LeafletGeoAdmin)
