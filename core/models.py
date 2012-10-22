# -*- coding: utf-8 -*-
from lxml import etree

from django.db import models
from django.db.models import Max, Count

# Create your models here.


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
    longtitude = models.FloatField()
    regionId = models.ForeignKey(Region, db_column='region_id')
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%f %f' % (self.latitude, self.longtitude)


class MessageType(models.Model):
    class Meta():
        db_table = 'message_type'

    name = models.CharField(max_length=100, db_column='name')
    slug = models.CharField(max_length=100, db_column='slug')

    def __unicode__(self):
        return self.name


class Message(models.Model):
    MESSAGE_STATUS = ((1, u'Новое'),
                      (2, u'Не подтверждено'),
                      (3, u'Подтверждено'),
                      (4, u'В работе'),
                      (6, u'Закрыто'))

    ACTIVE = 0
    IMPORTANT = 1
    ANONYMOUS = 2
    FEEDBACK = 3

    class Meta():
        db_table = 'Message'
        ordering = ['-dateAdd']

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Сообщение')
    dateAdd = models.DateTimeField(auto_now_add=True, db_column='date_add',
        editable=False)
    dateModify = models.DateTimeField(auto_now=True, db_column='date_modify',
        editable=False)
    locationId = models.ForeignKey(Location, db_column='location_id',
        null=True)
    status = models.SmallIntegerField(choices=MESSAGE_STATUS,
        verbose_name='Статус')
    flags = models.BigIntegerField()
    category = models.ManyToManyField(Category, db_table='messagecategories',
        symmetrical=False, verbose_name='Категории сообщения')
    subdomain = models.ForeignKey(Subdomain, db_column='subdomain_id',
        null=True, verbose_name='Страница атласа', blank=True)
    sender = models.TextField()
    messageType = models.ForeignKey(MessageType, db_column='message_type',
        verbose_name='Тип сообщения')
    notes = models.TextField(verbose_name='Заметки', blank=True, default='')

    def __unicode__(self):
        return self.title

    def get_sender(self):
        tree = etree.fromstring(self.sender)
        fn = tree[0].text or ''
        pn = tree[1].text or ''
        ln = tree[2].text or ''
        email = tree[3].text or ''
        #XXX Переделать на лямбда-функцию
        ph = []
        for e in tree[4:]:
            if e.tag == 'phone':
                ph.append(e.text or '')
        phones = ','.join(ph) or ''
        return u"%s %s %s, email: %s, тел: %s" % (ln, fn, pn, email, phones)

    def save(self, *args, **kwargs):
        self.locationId.save()
        super(Message, self).save(*args, **kwargs)

    def address(self, address=None):
        if address:
            self.locationId.name = address
        else:
            return self.locationId.name

    def latitude(self, lat=None):
        if lat:
            self.locationId.latitude = lat
        else:
            return self.locationId.latitude

    def longtitude(self, lon=None):
        if lon:
            self.locationId.longtitude = lon
        else:
            return self.locationId.longtitude

    def set_flag(self, flag, active):
        if active:
            self.flags = set_bit(self.flags, flag)
        else:
            self.flags = clear_bit(self.flags, flag)

    def active(self):
        return (self.flags & 1) == 1

    def important(self):
        return (self.flags & 2) == 2

    def anonymous(self):
        return (self.flags & 4) == 0

    def feedback(self):
        return (self.flags & 8) == 8

    def region(self, region=None):
        if region:
            self.locationId.regionId = region
        else:
            try:
                return self.locationId.regionId
            except:
                return Region.objects.get(id=50)

    def getImages(self):
        return Multimedia.objects.filter(message=self.id)

    def haveAttachment(self):
        a = Multimedia.objects.filter(message=self.id).count()
        return a > 0

    def is_removed(self):
        test = self.flags & 0x10
        return test != 0


class Multimedia(models.Model):
    class Meta():
        db_table = 'multimedia'

    link_type = models.SmallIntegerField(db_column='type')
    message = models.ForeignKey(Message, null=True, blank=True)
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

    message = models.ForeignKey(Message, db_column='message_id')
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
