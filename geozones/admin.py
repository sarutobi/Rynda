# -*- coding: utf-8 -*-

from django.contrib import admin
from olwidget.admin import GeoModelAdmin

from .models import Region


class RegionGeoModel(GeoModelAdmin):
    options = {
        'default_zoom': 6,
        'zoom_to_data_extent': False,
    }


admin.site.register(Region, RegionGeoModel)
