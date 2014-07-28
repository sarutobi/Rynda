# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


# class Subdomain(models.Model):
    # '''One atlas page'''
    # # Status of page
    # DISABLED = 0
    # ACTIVE = 1
    # ARCHIVED = 2

    # SUBDOMAIN_STATUS = (
        # (DISABLED, _('disabled')),
        # (ACTIVE, _('active')))

    # class Meta:
        # ordering = ['order']
        # verbose_name = _('map')
        # verbose_name_plural = _('maps')

    # url = models.CharField(max_length=50, blank=True, null=True)
    # title = models.CharField(max_length=50)
    # isCurrent = models.BooleanField(db_column='is_current')
    # status = models.SmallIntegerField(choices=SUBDOMAIN_STATUS)
    # order = models.IntegerField()
    # disclaimer = models.TextField(blank=True)

    # def __unicode__(self):
        # return self.title

    # def name(self):
        # return self.title

    # def full_url(self):
        # if self.url:
            # return "%s.newrynda.org" % self.url
        # else:
            # return "newrynda.org"


class Infopage(models.Model):
    class Meta:
        pass

    title = models.CharField(
        max_length=255, db_column='title',
        verbose_name=_('title'))
    text = models.TextField(db_column='text', verbose_name=_('text'))
    active = models.BooleanField(default=False, verbose_name=_('is active'))
    slug = models.SlugField(max_length=255, verbose_name=_('slug'))
    default = models.BooleanField(
        default=False, verbose_name=_('default page'))

    def __unicode__(self):
        return self.title
