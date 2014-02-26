# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

import django_filters
from core.models import Subdomain
from category.models import Category
from geozones.models import Location
from model_utils.managers import PassThroughManager


class MessageQueryset(QuerySet):
    def list(self):
        ''' Ask only few fields for listing'''
        return self.values(
            'id', 'title', 'message', 'messageType',
            'date_add', )

    def active(self):
        return self.filter(status__gt=Message.NEW, status__lt=Message.CLOSED)

    def closed(self):
        return self.filter(status=Message.CLOSED)

    def type_is(self, m_type):
        return self.filter(messageType=m_type)

    def subdomain_is(self, subdomain):
        return self.filter(subdomain__slug=subdomain)


class Message(models.Model):
    '''Message data'''

    class Meta():
        ordering = ['-date_add']
        get_latest_by = 'date_add'
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    # Message types
    REQUEST = 1
    OFFER = 2
    INFO = 3

    TYPES_CHOICE = (
        (REQUEST, _("request")),
        (OFFER, _("offer")),
        (INFO, _("informatial"))
    )

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

    # Managers
    objects = PassThroughManager.for_queryset_class(MessageQueryset)()

    # Основные поля сообщения
    title = models.CharField(
        max_length=200,
        verbose_name=_('title'),
        blank=True)
    message = models.TextField(verbose_name=_('message'))
    # Следующие два поля содержат контактную информацию человека, к которому
    # относится сообщение. Должно быть заполнено как минимум одно из этих
    # полей, это условие проверяется при записи данных в базу
    # NB! значения этих полей не обязательно должны совпадать с контактами
    # зарегистрированного пользователя, оставляющего сообщение.
    contact_mail = models.EmailField(max_length=254, blank=True, default='')
    contact_phone = models.CharField(max_length=10, blank=True, default='')
    # Тип сообщения, которое оставляет пользователь. Повлиять на это поле
    # пользователь не может, тип сообщения может изменить модератор.
    messageType = models.IntegerField(
        choices=TYPES_CHOICE,
        db_column='message_type',
        verbose_name=_('message type'),
    )
    # Ссылка на пользователя портала. Если сообщение
    # оставляет незарегистрированный пользователь, то тут будет ссылка
    # на пользователя settings.ANONYMOUS_USER_ID
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
        default=False, verbose_name=_('is virtual')
    )

    # Moderator's fields

    is_active = models.BooleanField(
        default=False, verbose_name=_('active')
    )
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

    #Links to core models
    linked_location = models.ForeignKey(
        Location,
        null=True, blank=True
    )
    category = models.ManyToManyField(
        Category,
        db_table='messagecategories',
        symmetrical=False,
        verbose_name=_("message categories"),
        null=True, blank=True
    )
    subdomain = models.ForeignKey(
        Subdomain, db_column='subdomain_id',
        null=True, blank=True,
        verbose_name=_('subdomain')
    )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Message, self).save(*args, **kwargs)

    def clean(self):
        """ проверка полей модели перед сохранением """
        if self.contact_mail == '' and self.contact_phone == '':
            raise ValidationError(
                _("You MUST provide an contact email or phone number!"))


class MessageSideFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['subdomain', 'messageType', 'category']


class MessageIndexFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['subdomain', 'date_add']

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
        return _("Note from %(user)s to message %(msgid)d")\
            % {'user': self.user, 'msgid': self.message_id, }
