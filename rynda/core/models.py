# -*- coding: utf-8 -*-

""" Core models """

from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SocialLinkType(models.Model):
    """ Social link type description """

    name = models.CharField(_("Name"), max_length=200)
    symbol = models.CharField(_("Symbol"), max_length=200, blank=True)

    def __unicode__(self):
        return self.name


class SiteSocialLinks(models.Model):
    """ Site specific social links """
    class Meta:
        ordering = ['ordering', ]
        verbose_name = _("Social link")
        verbose_name_plural = _("Social links")

    site = models.ForeignKey(Site, verbose_name=_("Site name"))
    social_link_type = models.ForeignKey(SocialLinkType, verbose_name=_('Link type'))
    help_title = models.CharField(_("Link title"), max_length=100)
    url = models.CharField(
        _("Link url"), max_length=2000,
        help_text=_("Include protocol, ex. 'mailto:email@host' for email")
    )
    ordering = models.IntegerField(_("Ordering"))

    def __unicode__(self):
        return self.social_link_type.name
