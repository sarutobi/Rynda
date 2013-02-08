# coding: utf-8

from django.db import models

from django.utils.translation import ugettext_lazy as _


class Region(models.Model):
    '''
    Common regional zones. All messages can be grouped by this territorial
    cluster.
    TODO: use django-mptt
    TODO: make nested regions
    TODO: link message to nested regions
    '''
    class Meta():
        ordering = ['order']

    # Region number
    name = models.CharField(max_length=200, verbose_name=_("region name"))
    # Region slug
    slug = models.SlugField(_("slug"))
    # Region center coordinates
    latitude = models.FloatField(_("latitude"))
    longitude = models.FloatField(_("longitude"))
    # Region map default zoom
    zoom = models.SmallIntegerField(_("map zoom"))
    order = models.IntegerField(_("order"))

    def __unicode__(self):
        return self.name

