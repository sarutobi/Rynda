# -*- coding: utf-8 -*-

from django.contrib import admin
from olwidget.admin import GeoModelAdmin

from .models import Region


admin.site.register(Region, GeoModelAdmin)


