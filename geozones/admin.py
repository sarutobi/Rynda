# -*- coding: utf-8 -*-

from django.contrib import admin
from olwidget.admin import GeoModelAdmin
from leaflet.admin import LeafletGeoAdmin

from .models import Region, Location


class RegionGeoModel(GeoModelAdmin):
    map_template = "geozones/olwidget/admin_olwidget.html"


# admin.site.register(Region, RegionGeoModel)
admin.site.register(Region, LeafletGeoAdmin)

admin.site.register(Location, LeafletGeoAdmin)
