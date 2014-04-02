# -*- coding: utf-8 -*-

from django.contrib import admin
from olwidget.admin import GeoModelAdmin

from .models import Region


class RegionGeoModel(GeoModelAdmin):
    map_template = "geozones/olwidget/admin_olwidget.html"


admin.site.register(Region, RegionGeoModel)
