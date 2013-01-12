# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#class Group(models.Model):
#    class Meta():
#        db_table = 'groups'
#        ordering = ['id']
#
#    id = models.IntegerField(db_column = 'id', primary_key = True)
#    name = models.CharField(max_length = 40, db_column = 'name')
#    description = models.CharField(max_length = 100, db_column = 'description')
#
#    def __unicode__(self):
#        return self.name

class Users(models.Model):
    '''Описание одного пользователя соцсети Рында'''
    class Meta():
        ordering = ['user']

    user = models.OneToOneField(User)
#    ipAddr = models.CharField(max_length = 16, db_column = 'ip_address')
#    email = models.EmailField(max_length = 100, db_column = 'email')
    activCode = models.CharField(max_length = 40,
        db_column = 'activation_code', null = True)
    forgotCode = models.CharField(max_length = 40,
        db_column = 'forgotten_password_code', null = True)
    rememberCode = models.CharField(max_length = 40,
        db_column = 'remember_code', null = True)
#    last_name = models.CharField(max_length=50, db_column='last_name')
    forgotten_time = models.DateTimeField(db_column='forgotten_password_time', null=True)
#    ref_type = models.IntegerField(db_column='ref_type', default=0)
    flags = models.IntegerField(db_column='flags', default=0)
    phones = models.CharField(max_length=255, blank=True)
    about_me = models.TextField(default='')
#     my_photo = models.IntegerField()
    birthday = models.DateField(null=True)
    gender = models.IntegerField(default=0)

#    def __unicode__(self):
#        return self.username



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Users.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


#class MetaUser(models.Model):
#    class Meta():
#        db_table = 'meta'
#
#    id = models.IntegerField(db_column = 'id', primary_key = True)
#    user = models.OneToOneField(Users, db_column = 'user_id')
#    firstName = models.CharField(max_length = 50, db_column = 'first_name')
#    lastName = models.CharField(max_length = 50, db_column = 'last_name')
#    flags = models.IntegerField(db_column = 'flags')
#
#    def __unicode__(self):
#        return "%s %s" % (self.lastName, self.firstName)
