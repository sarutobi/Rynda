# -*- coding: utf-8 -*-

from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Region, Location


# admin.site.register(Region, RegionGeoModel)
admin.site.register(Region, LeafletGeoAdmin)

admin.site.register(Location, LeafletGeoAdmin)
