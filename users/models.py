# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    class Meta():
        db_table = 'groups'
        ordering = ['id']

    id = models.IntegerField(db_column = 'id', primary_key = True)
    name = models.CharField(max_length = 40, db_column = 'name')
    description = models.CharField(max_length = 100, db_column = 'description')

    def __unicode__(self):
        return self.name

class Users(models.Model):
    '''Описание одного пользователя соцсети Рында'''
    class Meta():
        db_table = 'users'
        ordering = ['created']

    id = models.IntegerField(db_column = 'id', primary_key = True)
    user = models.OneToOneField(User)
    groupId = models.ForeignKey(Group, db_column = 'group_id')
    ipAddr = models.CharField(max_length = 16, db_column = 'ip_address')
    username = models.CharField(max_length = 15, db_column = 'username')
    password = models.CharField(max_length = 40, db_column = 'password')
    salt = models.CharField(max_length = 40, db_column = 'salt', null = True)
    email = models.EmailField(max_length = 100, db_column = 'email')
    activCode = models.CharField(max_length = 40, db_column = 'activation_code', null = True)
    forgotCode = models.CharField(max_length = 40, db_column = 'forgotten_password_code', null = True)
    rememberCode = models.CharField(max_length = 40, db_column = 'remember_code', null = True)
    created = models.IntegerField(db_column = 'created_on')
    lastLogin = models.IntegerField(db_column = 'last_login', null = True)
    active = models.NullBooleanField(db_column = 'active', null = True)
    first_name = models.CharField(max_length=50, db_column='first_name')
    last_name = models.CharField(max_length=50, db_column='last_name')
    forgotten_time = models.IntegerField(db_column='forgotten_password_time')
    ref_type = models.IntegerField(db_column='ref_type', default=0)
    flags = models.IntegerField(db_column='flags', default=0)
    phones = models.CharField(max_length=255, blank=True)
    about_me = models.TextField()
    my_photo = models.IntegerField()
    birthday = models.DateField()
    gender = models.IntegerField(default=0)
    ip_address = models.CharField(max_length=20)

    def __unicode__(self):
        return self.username

    def firstName(self):
        return self.first_name

    def lastName(self):
        return self.last_name

    def last_login(self):
        return datetime.fromtimestamp(self.lastLogin)

    def registered(self):
        return datetime.fromtimestamp(self.created)

class MetaUser(models.Model):
    class Meta():
        db_table = 'meta'

    id = models.IntegerField(db_column = 'id', primary_key = True)
    user = models.OneToOneField(Users, db_column = 'user_id')
    firstName = models.CharField(max_length = 50, db_column = 'first_name')
    lastName = models.CharField(max_length = 50, db_column = 'last_name')
    flags = models.IntegerField(db_column = 'flags')

    def __unicode__(self):
        return "%s %s" % (self.lastName, self.firstName)
