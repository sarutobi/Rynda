# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Region(models.Model):

    """
    Географический регион.

    Обобщенный георегион, описывающий произвольную геообласть на карте.
    Сообщения могут быть сгруппированы по этому признаку.
    TODO: use django-mptt
    TODO: make nested regions
    TODO: link message to nested regions

    """

    class Meta:
        ordering = ['order']
        verbose_name = _('region')
        verbose_name_plural = _('regions')

    # Region number
    name = models.CharField(
        max_length=200, verbose_name=_("region name"))
    # Region slug
    slug = models.SlugField(_("slug"))
    # Region center coordinates
    center = models.PointField(_("map center"), null=True)
    # Region map default zoom
    zoom = models.SmallIntegerField(_("map zoom"))
    order = models.IntegerField(_("order"))
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


class Location(models.Model):

    """
    Geolocation or POI.

    This data represent POI(Point Of Interest).
    Object contain small piece of data:
    * Geocoordinates - latitude and longitude
    * Description - textual name of POI or it's human-readable address
    * Optional link to georegion. If this link exists

    """

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    name = models.CharField(
        max_length=250, default='Location', verbose_name=_("name"))
    # Geocoordinates
    coordinates = models.GeometryCollectionField(
        null=True,
        verbose_name=_("On map"))
    # Optional link for region
    region = models.ForeignKey(
        Region,
        verbose_name=_("region"),
    )
    # Short description or address
    description = models.CharField(max_length=200, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name
