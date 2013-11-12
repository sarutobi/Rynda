# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
#from django.contrib.gis.db import models as geomodels
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

import django_filters

from model_utils.managers import PassThroughManager

from core.models import Category, Subdomain
from geozones.models import Region, Location


class MessageType(models.Model):
    '''Message types'''

    class Meta():
        verbose_name = _('message type')
        verbose_name_plural = _('message types')

    name = models.CharField(max_length=100, verbose_name=_('name'))
#    TYPE_REQUEST = 1
#    TYPE_OFFER = 2
#    TYPE_INFO = 3

#    TYPES_CHOICE = (
#        (TYPE_REQUEST, _("request")),
#        (TYPE_OFFER, _("offer")),
#        (TYPE_INFO, _("informatial"))
#    )


class MessageQueryset(QuerySet):
    def list(self):
        ''' Ask only few fields for listing'''
        return self.values(
            'id', 'title', 'message', 'messageType',
            'georegion', 'date_add', 'georegion__name')

    def active(self):
        return self.filter(status__gt=1, status__lt=6)

    def closed(self):
        return self.filter(status=6)

    def type_is(self, m_type):
        return self.filter(messageType=m_type)

    def subdomain_is(self, subdomain):
        return self.filter(subdomain__slug=subdomain)


class Message(models.Model):
    '''Message data'''
    #Flag values
    #MESSAGE_ACTIVE = 0x1L
    #MESSAGE_IMPORTANT = 0x2L
    #MESSAGE_NONANONYMOUS = 0x4L
    #ALLOW_FEEDBACK = 0x8L
    #MESSAGE_DELETED = 0x10L
    #LOCATION_VALID = 0x20L

    # Message status
    NEW = 1
    UNVERIFIED = 2
    VERIFIED = 3
    PENDING = 4
    CLOSED = 6

    MESSAGE_STATUS = ((NEW, _('new')),
                      (UNVERIFIED, _('unverified')),
                      (VERIFIED, _('verified')),
                      (PENDING, _('pending')),
                      (CLOSED, _('closed')))

    class Meta():
        ordering = ['-date_add']
        get_latest_by = 'date_add'
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    #Managers
    objects = PassThroughManager.for_queryset_class(MessageQueryset)()

    #Mandatory fields
    title = models.CharField(
        max_length=200,
        verbose_name=_('title'),
        blank=True)
    message = models.TextField(verbose_name=_('message'))
    messageType = models.ForeignKey(
        MessageType,
        db_column='message_type',
        verbose_name=_('message type'),)
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        editable=False,
        db_column='user_id',)
    georegion = models.ForeignKey(Region, verbose_name=_('region'))
    #location = geomodels.PointField(
    #    _('location'),
    #    geography=True,
    #    blank=True, null=True)
    address = models.CharField(max_length=200, verbose_name=_('address'))
    # Optional fields
    # Message original source
    source = models.CharField(
        max_length=255,
        verbose_name=_("source"),
        blank=True)

    # Moderator's fields
    #flags = models.BigIntegerField(default=0)
    is_active = models.BooleanField(
        default=False, verbose_name=_('active'))
    is_important = models.BooleanField(
        default=False, verbose_name=_('important'))
    is_anonymous = models.BooleanField(
        default=True, verbose_name=_('hide contacts'))
    is_removed = models.BooleanField(
        default=False, verbose_name=_('removed'))
    allow_feedback = models.BooleanField(
        default=True, verbose_name=_('allow feedback'))

    status = models.SmallIntegerField(
        choices=MESSAGE_STATUS,
        verbose_name=_('status'),
        default=1, blank=True, null=True)

    #Internal fields
    date_add = models.DateTimeField(
        auto_now_add=True,
        db_column='date_add',
        editable=False)
    last_edit = models.DateTimeField(
        auto_now=True,
        db_column='date_modify',
        editable=False)
    expired_date = models.DateTimeField(
        verbose_name=_("expired at"),
        blank=True, null=True)
    edit_key = models.CharField(max_length=40, blank=True)
    sender_ip = models.IPAddressField(
        blank=True, null=True,
        editable=False,
        verbose_name=_("sender IP"))

    #Links to core models
    linked_location = models.ForeignKey(
        Location,
        null=True, blank=True)
    category = models.ManyToManyField(
        Category,
        db_table='messagecategories',
        symmetrical=False,
        verbose_name=_("message categories"),
        null=True,
        blank=True)
    subdomain = models.ForeignKey(
        Subdomain, db_column='subdomain_id',
        null=True, blank=True,
        verbose_name=_('subdomain'))

    # Gis queries
    #gis = geomodels.GeoManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Message, self).save(*args, **kwargs)


class MessageSideFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['georegion', 'subdomain', 'messageType', 'category']


class MessageIndexFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['georegion', 'subdomain', 'date_add']

    date_add = django_filters.DateRangeFilter()


class MessageNotes(models.Model):
    '''Moderator notes for message'''
    message = models.ForeignKey(Message)
    user = models.ForeignKey(User, editable=False, verbose_name=_("author"))
    note = models.TextField(verbose_name=_("note"))
    date_add = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("created at"))
    last_edit = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_("last edit"))

    def __unicode__(self):
        return "Note from %s" % self.user
