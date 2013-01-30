# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from core.models import Location, Category, Subdomain


class ApprovedMessages(models.Manager):
    def get_query_set(self):
        return super(ApprovedMessages, self).get_query_set()\
            .filter(status__gt=1)


class MessageType(models.Model):
    '''Message types'''
    class Meta():
        db_table = 'message_type'

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    icon = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Message(models.Model):
    '''Message data'''
    #Flag values
    MESSAGE_ACTIVE = 0x1L
    MESSAGE_IMPORTANT = 0x2L
    MESSAGE_NONANONYMOUS = 0x4L
    ALLOW_FEEDBACK = 0x8L
    MESSAGE_DELETED = 0x10L
    LOCATION_VALID = 0x20L

    MESSAGE_STATUS = ((1, u'Новое'),
                      (2, u'Не подтверждено'),
                      (3, u'Подтверждено'),
                      (4, u'В работе'),
                      (6, u'Закрыто'))

    class Meta():
        ordering = ['-date_add']

    #Managers
    objects = models.Manager()
    approved = ApprovedMessages()

    #Mandatory fields
    title = models.CharField(max_length=200, verbose_name='Заголовок', blank=True)
    message = models.TextField(verbose_name='Сообщение')
    contact_first_name = models.CharField(max_length=200, verbose_name="First name",
        blank=True)
    contact_last_name = models.CharField(max_length=200, verbose_name="Last name",
        blank=True)
    contact_mail = models.CharField(max_length=200, blank=True,
        verbose_name="Email(s)", validators=[validate_email])
    contact_phone = models.CharField(max_length=200, blank=True,
        verbose_name="Phone(s)")
    messageType = models.ForeignKey(MessageType, db_column='message_type',
        verbose_name='Тип сообщения', blank=True, null=True)

    #Optional fields
    source = models.CharField(max_length=255, verbose_name="Source",
        blank=True)

    #Moderator's fields
    flags = models.BigIntegerField(default=0, blank=True)
    status = models.SmallIntegerField(choices=MESSAGE_STATUS,
        verbose_name='Статус', default=1, blank=True)

    #Internal fields
    date_add = models.DateTimeField(auto_now_add=True,
        db_column='date_add', editable=False)
    last_edit = models.DateTimeField(auto_now=True,
        db_column='date_modify', editable = False)
    expired_date = models.DateTimeField(verbose_name="Expired at",
        blank=True, null=True)
    user = models.IntegerField(verbose_name="User", editable=False,
        db_column='user_id', null=True, blank=True)
    edit_key = models.CharField(max_length=40, blank=True)
    sender_ip = models.IPAddressField(blank=True, null=True, editable=False,
        verbose_name="Sender IP")

    #Links to core models
    location = models.ForeignKey(Location, db_column='location_id',
        null=True, blank=True)
    category = models.ManyToManyField(Category, db_table='messagecategories',
        symmetrical=False, verbose_name='Категории сообщения', null=True,
        blank=True)
    subdomain = models.ForeignKey(Subdomain, db_column='subdomain_id',
        null=True, blank=True, verbose_name='Страница атласа')

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

    def clean(self):
        if not self.contact_mail and not self.contact_phone:
            raise ValidationError("You must provide email or phone!")

    def save(self, *args, **kwargs):
        self.full_clean()
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


class MessageNotes(models.Model):
    '''Moderator notes for message'''
    message = models.ForeignKey(Message)
    user = models.IntegerField()
    note = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True, editable=False)
    last_edit = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return "Note from %s" % self.user
