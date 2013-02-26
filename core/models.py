# coding: utf-8

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _


class Subdomain(models.Model):
    '''One atlas page'''
    SUBDOMAIN_STATUS = (
        (0, _('inactive')),
        (1, _('active')))

    class Meta:
        ordering = ['order']

    url = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=50)
    isCurrent = models.BooleanField(db_column='is_current')
    status = models.SmallIntegerField(choices=SUBDOMAIN_STATUS)
    order = models.IntegerField()
    disclaimer = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    def name(self):
        return self.title

    def full_url(self):
        if self.url:
            return "%s.newrynda.org" % self.url
        else:
            return "newrynda.org"


class Category(models.Model):
    ''' Категория сообщения '''
    class Meta:
        ordering = ['order']

    parentId = models.ForeignKey(
        'self', default=0, db_column='parent_id',
        verbose_name=_('parent category'), blank=True, null=True,
        related_name='parent')
    name = models.CharField(
        max_length=200, db_column='name',
        verbose_name=_('name'))
    description = models.TextField(
        blank=True, db_column='description',
        verbose_name=_('description'))
    color = models.CharField(
        max_length=7, db_column='color',
        default='#000000', verbose_name=_('color'))
    slug = models.SlugField(
        max_length=255, db_column='slug',
        verbose_name=_('slug'), blank=True)
    icon = models.CharField(
        max_length=255, null=True, blank=True,
        db_column='icon', verbose_name=_('icon'))
    order = models.SmallIntegerField(db_column='order')
    subdomain = models.ForeignKey(
        Subdomain, null=True, blank=True,
        db_column='subdomain_id', verbose_name=_('subdomain'))
    group = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class CategoryLinks(models.Model):
    ''' Links categories for generic models'''
    category = models.ForeignKey(Category)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')


class Infopage(models.Model):
    class Meta:
        pass

    title = models.CharField(
        max_length=255, db_column='title',
        verbose_name=_('title'))
    text = models.TextField(db_column='text', verbose_name=_('text'))
    active = models.BooleanField(default=False, verbose_name=_('is active'))
    slug = models.SlugField(max_length=255, verbose_name=_('slug'))

    def __unicode__(self):
        return self.title
