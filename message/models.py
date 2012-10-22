# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.



class MessageType(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    icon = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Message(models.Model):
    #Flags values
    MESSAGE_ACTIVE = 0x1L
    MESSAGE_IMPORTANT = 0x2L
    MESSAGE_NONANONYMOUS = 0x4L
    ALLOW_FEEDBACK = 0x8L
    MESSAGE_DELETED = 0x10L
    LOCATION_VALID = 0x20L

    #Message types
    MESSAGE_TYPE = (
        (1, "Request"),
        (2, "Offer"),
        (3, "Information"),
        (4, "Advise"),
        (5, "Event"),
    )

    MESSAGE_STATUS = (
        (1, "New"),
        (2, "Unverified"),
        (3, "Verified"),
        (4, "In progress"),
        (5, "Closed")
    )
    #Mandatory fields
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    message = models.TextField(verbose_name = 'Сообщение')
    contact = models.CharField(max_length=200, verbose_name="Author",
        blank=True, null=True)
    contact_mail = models.CharField(max_length=200, blank=True,
        null=True, verbose_name="Email(s)")
    contact_phone = models.CharField(max_length=200,blank=True,
        null=True, verbose_name="Phone(s)")
    messageType = models.SmallIntegerField(choices=MESSAGE_TYPE, db_column='message_type',
        verbose_name='Тип сообщения')

    #Optional fields
    source = models.CharField(max_length=255, verbose_name="Source",
        null=True, blank=True)
    
    #Moderator's fields
    flags = models.BigIntegerField()
    status = models.SmallIntegerField(choices=MESSAGE_STATUS, verbose_name='Статус')

    #Internal fields    
    date_add = models.DateTimeField(auto_now_add=True, 
        db_column='date_add', editable=False)
    last_edit = models.DateTimeField(auto_now=True,
        db_column='date_modify', editable = False)
    expired_date = models.DateTimeField(verbose_name="Expired at",
        blank=True, null=True)
    user = models.IntegerField(verbose_name="User", editable=False)
    edit_key = models.CharField(max_length=20)

    #locationId = models.ForeignKey(Location, db_column = 'location_id', null = True)
    #category = models.ManyToManyField(Category, db_table = 'messagecategories', symmetrical = False, verbose_name = 'Категории сообщения')
    #subdomain = models.ForeignKey(Subdomain, db_column = 'subdomain_id', null = True, verbose_name = 'Страница атласа', blank = True)

    def __unicode__(self):
        return self.title


class MessageNotes(models.Model):
    '''Moderator notes for message'''
    message = models.ForeignKey(Message)
    user = models.IntegerField()
    note = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True, editable=False)
    last_edit = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return "Note from %s" % self.user
