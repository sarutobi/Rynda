# -*- coding: utf-8 -*-

from django.contrib import admin
from olwidget.admin import GeoModelAdmin
from olwidget.forms import MapModelForm

from .models import Region


class RegionAdminForm(MapModelForm):
    """ Форма редактирования региона для админки """
    class Meta:
        # model = Region
        template = "geozones/olwidget/admin_olwidget.html"


class RegionGeoModel(GeoModelAdmin):
    # form = RegionAdminForm
    map_template = "geozones/olwidget/admin_olwidget.html"


admin.site.register(Region, RegionGeoModel)
