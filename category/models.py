# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import Subdomain


class Category(models.Model):
    """ Категория сообщения """
    class Meta:
        ordering = ['order']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

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
    group = models.ForeignKey("CategoryGroup", null=True, blank=True)

    def __unicode__(self):
        return self.name

    def unlink(self):
        '''Remove link to category group'''
        self.group = None
        self.save()


class CategoryGroup(models.Model):
    """ Модель для группировки категорий """
    class Meta:
        ordering = ['order']
        verbose_name = _('category group')
        verbose_name_plural = _('category groups')

    name = models.CharField(
        max_length=200,
        verbose_name=_('category group name'))
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    def add_category(self, category):
        """ Добавляет категорию в группу """
        category.group = self
        category.save()
