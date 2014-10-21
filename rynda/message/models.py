# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

from geozones.models import Location
from model_utils.managers import PassThroughManagerMixin


class Category(models.Model):
    """ Message categories """
    class Meta:
        ordering = ['order']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    name = models.CharField(
        max_length=200, db_column='name',
        verbose_name=_('name'))
    description = models.TextField(
        blank=True, db_column='description',
        verbose_name=_('description'))
    slug = models.SlugField(
        max_length=255, db_column='slug',
        verbose_name=_('slug'), blank=True)
    order = models.SmallIntegerField(db_column='order')

    def __unicode__(self):
        return self.name


class PassThroughGeoManager(PassThroughManagerMixin, models.GeoManager):
    pass


class MessageQueryset(GeoQuerySet):
    def list(self):
        """ Ask only few fields for listing"""

        return self.values(
            'id', 'title', 'message', 'messageType',
            'date_add', )

    def active(self):
        return self.filter(
            status__gt=Message.NEW, status__lt=Message.CLOSED,
            is_removed=False
        )

    def closed(self):
        return self.filter(status=Message.CLOSED)

    def type_is(self, m_type):
        return self.filter(messageType=m_type)

    def is_deleted(self):
        return self.filter(is_removed=True)


class Message(models.Model):
    """ Message data """

    class Meta():
        ordering = ['-date_add']
        get_latest_by = 'date_add'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    # Message types
    REQUEST = 1
    OFFER = 2
    INFO = 3

    TYPES_CHOICE = (
        (REQUEST, _("Request message")),
        (OFFER, _("Offer message")),
        # (INFO, _("Informatial message"))
    )

    # Message status
    NEW = 1
    UNVERIFIED = 2
    VERIFIED = 3
    PENDING = 4
    CLOSED = 6

    MESSAGE_STATUS = ((NEW, _('New')),
                      (UNVERIFIED, _('Unverified')),
                      (VERIFIED, _('Verified')),
                      (PENDING, _('Pending')),
                      (CLOSED, _('Closed')))

    # Managers
    objects = PassThroughGeoManager.for_queryset_class(MessageQueryset)()

    # Main message fields
    title = models.CharField(
        max_length=200,
        verbose_name=_('title'),
        blank=True)
    message = models.TextField(verbose_name=_('Message'))
    # Additional message information. This is important for message, but
    # useless for engine.
    additional_info = JSONField(
        blank=True, default='', verbose_name=_("Additional info"))
    # Message type. Only moderator can change this type.
    messageType = models.IntegerField(
        choices=TYPES_CHOICE,
        db_column='message_type',
        verbose_name=_('Message type'),
    )
    # Link to message author. It can be anonymous for engine, so this will be
    # link to settings.ANONYMOUS_USER_ID
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        editable=False,
        db_column='user_id',
    )

    # Optional fields
    # Message original source
    source = models.CharField(
        max_length=255,
        verbose_name=_("source"),
        blank=True
    )

    is_virtual = models.BooleanField(
        default=False, verbose_name=_('Is virtual')
    )

    # Moderator's fields
    # Message can be inactive, i.e. not 'closed' and no more information can be
    # added.
    is_active = models.BooleanField(
        default=False, verbose_name=_('active')
    )
    # Is it urgent message?
    is_important = models.BooleanField(
        default=False, verbose_name=_('important')
    )
    is_anonymous = models.BooleanField(
        default=True, verbose_name=_('hide contacts')
    )
    is_removed = models.BooleanField(
        default=False, verbose_name=_('removed')
    )
    allow_feedback = models.BooleanField(
        default=True, verbose_name=_('allow feedback')
    )

    status = models.SmallIntegerField(
        choices=MESSAGE_STATUS,
        verbose_name=_('status'),
        default=NEW, blank=True, null=True
    )

    #Internal fields
    date_add = models.DateTimeField(
        auto_now_add=True,
        db_column='date_add',
        editable=False
    )
    last_edit = models.DateTimeField(
        auto_now=True,
        db_column='date_modify',
        editable=False
    )
    expired_date = models.DateTimeField(
        verbose_name=_("expired at"),
        blank=True, null=True
    )
    edit_key = models.CharField(max_length=40, blank=True)
    sender_ip = models.IPAddressField(
        blank=True, null=True,
        editable=False,
        verbose_name=_("sender IP")
    )

    # Links to core models
    linked_location = models.ForeignKey(
        Location,
        null=True, blank=True
    )
    category = models.ManyToManyField(
        Category,
        symmetrical=False,
        verbose_name=_("message categories"),
        null=True, blank=True
    )

    def __unicode__(self):
        return self.title or "Untitled"

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Message, self).save(*args, **kwargs)

    def get_sender_name(self):
        """ Format sender name based on is_anonymous flag """

        first_name = self.additional_info['first_name'].capitalize()
        last_name = self.additional_info['last_name'].capitalize()
        if self.is_anonymous and last_name:
            last_name = last_name[0]
        return "%s %s" % (first_name, last_name)

    def get_absolute_url(self):
        return reverse_lazy("message-details", args=[str(self.pk)])


class MessageNotes(models.Model):
    """ Moderator notes for message """

    message = models.ForeignKey(Message)
    user = models.ForeignKey(User, editable=False, verbose_name=_("Author"))
    note = models.TextField(verbose_name=_("Note"))
    date_add = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Created at"))
    last_edit = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_("Last edit"))

    def __unicode__(self):
        return _("Note from %(user)s to message %(msgid)d")\
            % {'user': self.user, 'msgid': self.message_id, }
