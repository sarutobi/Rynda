# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.gis.db import models as geomodels
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import PassThroughManager

from core.models import Category, Subdomain
from geozones.models import Region, Location


class MessageType():
    '''Message types'''

    TYPE_REQUEST = 1
    TYPE_RESPONSE = 2
    TYPE_INFO = 3

    TYPES_CHOICE = (
        (TYPE_REQUEST, _("request")),
        (TYPE_RESPONSE, _("response")),
        (TYPE_INFO, _("informatial"))
    )


class MessageQueryset(QuerySet):
    def list(self):
        ''' Ask only few fields for listing'''
        return self.values(
            'id', 'title', 'message', 'messageType', 'georegion', 'date_add')

    def active(self):
        return self.filter(status__gt=1, status__lt=6)

    def closed(self):
        return self.filter(status=6)


class Message(geomodels.Model):
    '''Message data'''
    #Flag values
    MESSAGE_ACTIVE = 0x1L
    MESSAGE_IMPORTANT = 0x2L
    MESSAGE_NONANONYMOUS = 0x4L
    ALLOW_FEEDBACK = 0x8L
    MESSAGE_DELETED = 0x10L
    LOCATION_VALID = 0x20L

    MESSAGE_STATUS = ((1, _('new')),
                      (2, _('unverified')),
                      (3, _('verified')),
                      (4, _('pending')),
                      (6, _('closed')))

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
    contact_first_name = models.CharField(
        max_length=200,
        verbose_name=_("first name"))
    contact_last_name = models.CharField(
        max_length=200,
        verbose_name=_("last name"))
    contact_mail = models.EmailField(
        max_length=200,
        blank=True,
        verbose_name=_("email(s)"))
    contact_phone = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("phone(s)"))
    messageType = models.IntegerField(
        choices=MessageType.TYPES_CHOICE,
        db_column='message_type',
        verbose_name=_('message type'),)
    georegion = models.ForeignKey(Region, verbose_name=_('region'))
    location = geomodels.PointField(
        _('location'),
        geography=True,
        blank=True, null=True)
    # Optional fields
    # Message original source
    source = models.CharField(
        max_length=255,
        verbose_name=_("source"),
        blank=True)

    # Moderator's fields
    flags = models.BigIntegerField(default=0, blank=True)
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
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        editable=False,
        db_column='user_id',
        null=True, blank=True)
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
    gis = geomodels.GeoManager()

    def __unicode__(self):
        return self.title

    def remove(self):
        self.flags = self.flags | self.MESSAGE_DELETED

    def restore(self):
        mask = ~self.MESSAGE_DELETED
        self.flags = self.flags & mask

    def clean(self):
        if not self.contact_mail and not self.contact_phone:
            raise ValidationError("You must provide email or phone!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Message, self).save(*args, **kwargs)

    #def address(self, address=None):
    #    if address:
    #        self.locationId.name = address
    #    else:
    #        return self.locationId.name

    #def latitude(self, lat=None):
    #    if lat:
    #        self.locationId.latitude = lat
    #    else:
    #        return self.locationId.latitude

    #def longtitude(self, lon=None):
    #    if lon:
    #        self.locationId.longtitude = lon
    #    else:
    #        return self.locationId.longtitude

    #def set_flag(self, flag, active):
    #    if active:
    #        self.flags = set_bit(self.flags, flag)
    #    else:
    #        self.flags = clear_bit(self.flags, flag)

    def is_removed(self):
        return (self.flags & self.MESSAGE_DELETED) == self.MESSAGE_DELETED



    #def active(self):
    #    return (self.flags & 1) == 1

    #def important(self):
    #    return (self.flags & 2) == 2

    #def anonymous(self):
    #    return (self.flags & 4) == 0

    #def feedback(self):
    #    return (self.flags & 8) == 8

    #def region(self, region=None):
    #    if region:
    #        self.locationId.regionId = region
    #    else:
    #        try:
    #            return self.locationId.regionId
    #        except:
    #            return Region.objects.get(id=50)

    #def getImages(self):
    #    return Multimedia.objects.filter(message=self.id)

    #def haveAttachment(self):
    #    a = Multimedia.objects.filter(message=self.id).count()
    #    return a > 0


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
