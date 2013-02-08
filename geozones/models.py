# coding: utf-8

from django.db import models

from django.utils.translation import ugettext_lazy as _


class Region(models.Model):
    '''
    Region
    ======
    Common regional zones. All messages can be grouped by this territorial
    cluster.
    * TODO: use django-mptt
    * TODO: make nested regions
    * TODO: link message to nested regions
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


class Location(models.Model):
    '''
    Geolocation
    ===========
    This data represent POI(Point Of Interest).
    Object contain small piece of data:
    * Geocoordinates - latitude and longitude
    * Description - textual name of POI or it's human-readable address
    * Optional link to georegion. If this link exists
    '''
    # Geocoordinates
    latitude = models.FloatField()
    longitude = models.FloatField(db_column='longitude')
    # Optional link for region
    region = models.ForeignKey(
        Region,
        verbose_name=_("region"),
        null=True, blank=True)
    # Short description or address
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%f %f' % (self.latitude, self.longitude)


