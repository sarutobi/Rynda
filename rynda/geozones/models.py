# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
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
        max_length=200, verbose_name=_("Region"))
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
