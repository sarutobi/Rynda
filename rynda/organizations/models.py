# -*- coding: utf-8 -*-

from django.db import models
from core.models import Location


class OrganizationType(models.Model):
    '''Типы организаций'''
    class Meta():
        db_table = 'organization_type'
        ordering = ['id']

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Organization(models.Model):
    ''' Описание одной организации'''
    class Meta():
        db_table = 'organization'
        ordering = ['name', '-dateAdd']

    orgType = models.ForeignKey(OrganizationType, db_column='type',
        verbose_name='Тип организации')
    name = models.CharField(max_length=255,
        verbose_name='Наименование организации')
    description = models.TextField(verbose_name='Описание организации')
    locationId = models.ForeignKey(Location, db_column='location_id')
    dateAdd = models.DateTimeField(db_column='date_add')
    phone = models.CharField(max_length=255, verbose_name='Список телефонов')
    email = models.CharField(max_length=255, verbose_name='Список e-mail',
        blank=True)
    site = models.CharField(max_length=255, verbose_name='Список сайтов',
        blank=True)
    contacts = models.CharField(max_length=255, verbose_name='Контакты',
        blank=True)
    category = models.ManyToManyField(Category,
        db_table='organization_categories', symmetrical=False,
        verbose_name='Категории')

    def region(self, region=None):
        if region:
            self.locationId.regionId = region
        else:
            return self.locationId.regionId

    def latitude(self, latitude=None):
        if latitude:
            self.locationId.latitude = latitude
        else:
            return self.locationId.latitude

    def longtitude(self, longtitude=None):
        if longtitude:
            self.locationId.longtitude = longtitude
        else:
            return self.locationId.longtitude

    def address(self, address=None):
        if address is not None:
            self.locationId.name = address
        else:
            return self.locationId.name

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.locationId.save()
        super(Organization, self).save(*args, **kwargs)

    @staticmethod
    def NamesIndex():
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select distinct upper(substring(name, 1, 1))\
            from organization")
        rows = cursor.fetchall()
        s = u''
        rows.sort()
        for l in rows:
            s += l[0]
        return s
