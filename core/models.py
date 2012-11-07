# -*- coding: utf-8 -*-
from lxml import etree

from django.db import models
from django.db.models import Max, Count


class Subdomain(models.Model):
    '''Описание субдоменов для работы со страничками атласа'''
    SUBDOMAIN_STATUS = ((0, u'Неактивен'),
                        (1, u'Активен'),
    )

    class Meta():
        db_table = 'subdomain'
        ordering = ['order']

    url = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=50)
    isCurrent = models.BooleanField(db_column='is_current')
    status = models.SmallIntegerField(choices=SUBDOMAIN_STATUS)
    order = models.IntegerField()
    disclaimer = models.TextField(blank=True, null=True)

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
    class Meta():
        db_table = "Category"
        ordering = ['order']

    parentId = models.ForeignKey('self', default=0, db_column='parent_id',
        verbose_name='Родительская категория', blank=True, null=True)
    name = models.CharField(max_length=200, db_column='name',
        verbose_name='Наименование категории')
    description = models.TextField(null=True, db_column='description',
        verbose_name='Описание категории')
    color = models.CharField(max_length=7, db_column='color',
        default='#000000', verbose_name='Цвет категории')
    slug = models.SlugField(max_length=255, db_column='slug',
        verbose_name='Имя для ссылки', blank=True)
    icon = models.CharField(max_length=255, null=True, blank=True,
        db_column='icon', verbose_name='Иконка')
    order = models.SmallIntegerField(db_column='order')
    subdomain = models.ForeignKey(Subdomain, null=True, blank=True,
        db_column='subdomain_id', verbose_name='Страница атласа')

    def __unicode__(self):
        return self.name

class Infopage(models.Model):
    class Meta():
        db_table = 'information_page'

    title = models.CharField(max_length=255, db_column='title')
    text = models.TextField(db_column='text')
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255)

    def __unicode__(self):
        return self.title


class City(models.Model):
    class Meta():
        db_table = 'City'

    region_id = models.ForeignKey('Region', db_column='region_id')
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longtitude = models.FloatField()

    def __unicode__(self):
        return self.name


class Region(models.Model):
    class Meta():
        db_table = 'Region'
        ordering = ['order']

    name = models.CharField(max_length=200)
    cityId = models.ForeignKey(City, db_column='city_id')
    slug = models.SlugField()
    zoomLvl = models.SmallIntegerField(db_column='zoom_lvl')
    order = models.IntegerField()

    def __unicode__(self):
        return self.name


class Location(models.Model):
    class Meta():
        db_table = 'Location'

    latitude = models.FloatField()
    longitude = models.FloatField(db_column='longitude')
    regionId = models.ForeignKey(Region, db_column='region_id')
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%f %f' % (self.latitude, self.longtitude)


class Multimedia(models.Model):
    class Meta():
        db_table = 'multimedia'

    link_type = models.SmallIntegerField(db_column='type')
    message = models.ForeignKey('message.Message', null=True, blank=True)
    uri = models.CharField(max_length=255)
    thumb_uri = models.CharField(max_length=255)
    checksum = models.CharField(max_length=40)

    def __unicode__(self):
        return self.uri


class Comment(models.Model):
    '''Базовый комментарий'''
    class Meta:
        db_table = 'comment'

    message = models.TextField()
    dateAdd = models.DateTimeField(db_column='date_add')
    status = models.IntegerField()
    sender = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    ip = models.CharField(max_length=20)

    def __unicode__(self):
        return "Comment from %s" % self.sender


class MessageComment(models.Model):
    '''Привязка комментария к сообщению'''
    class Meta:
        db_table = 'in_reply_to'

    message = models.ForeignKey('message.Message', db_column='message_id')
    comment = models.OneToOneField(Comment, db_column='comment_id',
        related_name='comment')
    reply = models.ForeignKey(Comment, db_column='reply_to',
        related_name='reply_to', blank=True, null=True)
    level = models.IntegerField()

    def __unicode__(self):
        return "Comment %s reply to %s" % (self.comment_id, self.reply_id)


def set_bit(int_type, offset):
    mask = 1 << offset
    return (int_type | mask)


def clear_bit(int_type, offset):
    mask = ~(1 << offset)
    return (int_type & mask)
