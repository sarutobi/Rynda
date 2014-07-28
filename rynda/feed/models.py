#-*- coding: utf-8 -*-

from django.db import models

class Feed(models.Model):
    '''Описатель одного РСС-потока'''
    class Meta():
        db_table = 'feed'

    name = models.CharField(max_length = 100)
    url = models.CharField(max_length = 255 )
    status = models.SmallIntegerField()
    lastActivity = models.DateTimeField(db_column = 'last_activity')

    def __unicode__(self):
        return self.name

class FeedItem(models.Model):
    '''Одно сообщение из ленты сообщений'''
    class Meta():
        db_table = 'feed_item'
        ordering = ['-date']

    feedId = models.ForeignKey(Feed, db_column = 'feed_id')
    title = models.CharField(max_length = 255)
    content = models.TextField(null = True)
    link = models.CharField(max_length = 255, null = True)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.title
