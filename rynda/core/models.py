# -*- coding: utf-8 -*-

""" Core models """

from django.contrib.sites.models import Site
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.utils.translation import ugettext_lazy as _


class SocialLinkType(models.Model):
    """ Social link type description """
    class Meta:
        verbose_name = _("Contact type")
        verbose_name_plural = _("Contact types")

    name = models.CharField(_("Name"), max_length=200)
    symbol = models.CharField(_("Symbol"), max_length=200, blank=True)

    def __unicode__(self):
        return self.name


class SiteSocialLinks(models.Model):
    """ Site specific social links """
    class Meta:
        ordering = ['ordering', ]
        verbose_name = _("Site contact")
        verbose_name_plural = _("Site contacts")

    site = models.ForeignKey(Site, verbose_name=_("Site name"), on_delete=models.CASCADE)
    social_link_type = models.ForeignKey(SocialLinkType, verbose_name=_('Link type'), on_delete=models.CASCADE)
    help_title = models.CharField(_("Link title"), max_length=100)
    url = models.CharField(
        _("Link url"), max_length=2000,
        help_text=_("Include protocol, ex. 'mailto:email@host' for email")
    )
    ordering = models.IntegerField(_("Ordering"))

    def __unicode__(self):
        return self.social_link_type.name


class SiteMapOptions(geomodels.Model):
    """ Site specific map options """
    class Meta:
        verbose_name = _("Site map options")

    site = geomodels.OneToOneField(Site, verbose_name=_("Site name"), on_delete=models.CASCADE)
    zoom = geomodels.SmallIntegerField(verbose_name=_("Map zoom"), default=3)
    center = geomodels.PointField(verbose_name=_("Default map center"))
