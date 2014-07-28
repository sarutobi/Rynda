# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Max, Count

from geozones.models import Region


class City(models.Model):
    class Meta():
        db_table = 'City'

    region_id = models.ForeignKey(Region, db_column='region_id')
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longtitude = models.FloatField()

    def __unicode__(self):
        return self.name



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
