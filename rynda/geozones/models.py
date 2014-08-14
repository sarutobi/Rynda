# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.contrib.gis.geos import GeometryCollection
from django.utils.translation import ugettext_lazy as _


class Region(models.Model):

    """
    A georegion.

    An abstract georegion, that describes map geozone. Any messages can be
    clustered by this item.
    TODO: auto link Location to regions

    """

    class Meta:
        ordering = ['order']
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')

    # Region number
    name = models.CharField(
        max_length=200, verbose_name=_("Region name"))
    # Region slug
    slug = models.SlugField(_("slug"))
    # Region center coordinates
    center = models.PointField(_("Map center"), null=True)
    # Region map default zoom
    zoom = models.SmallIntegerField(_("Map zoom"))
    order = models.IntegerField(_("Order"))
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
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    name = models.CharField(
        max_length=250, default='Location', verbose_name=_("Name"))
    # Geocoordinates
    coordinates = models.GeometryCollectionField(
        null=True,
        verbose_name=_("On map"))
    # Optional link for region
    region = models.ForeignKey(
        Region,
        verbose_name=_("Region"),
        blank=True, null=True,
    )
    # Short description or address
    description = models.CharField(max_length=200, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    def to_geocollection(self, geodata):
        self.coordinates = GeometryCollection(geodata)
