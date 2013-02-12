# -*- coding: utf-8 -*-

import random
import base64
import hashlib
import string

from django.db import models
from django.contrib.auth.models import User

from templated_emails.utils import send_templated_email

from core.backends import IonAuth


class UserAuthCode(object):
    def __init__(self, secret, salt_len=8, hash=hashlib.sha256):
        self.secret = secret
        self.salt_len = salt_len
        self.hash = hash

    def salt(self):
        s = [random.choice(string.letters + string.digits)
             for i in xrange(self.salt_len)]
        return "".join(s)

    def digest(self, user, salt):
        # Use username, email and date_joined to generate digest
        auth_message = ''.join((self.secret, user.username, user.email,
                               str(user.date_joined), salt))
        md = self.hash()
        md.update(auth_message)

        return base64.urlsafe_b64encode(md.digest()).rstrip('=')

    def auth_code(self, user):
        salt = self.salt()
        digest = self.digest(user, salt)

        return "%s%s" % (salt, digest)

    def is_valid(self, user, auth_code):
        #import pdb; pdb.set_trace()
        salt = auth_code[:self.salt_len]
        digest = auth_code[self.salt_len:]

        # CAVEAT: Make sure UserAuthCode cannot be used to reactivate locked
        # profiles.
        if user.last_login >= user.date_joined:
            return False

        return digest == self.digest(user, salt)


class Profile(models.Model):
    '''
    User profile
    '''
    class Meta():
        ordering = ['user']

    user = models.OneToOneField(User)
#    ipAddr = models.CharField(max_length = 16, db_column = 'ip_address')
#    email = models.EmailField(max_length = 100, db_column = 'email')
    activCode = models.CharField(
        max_length=40,
        db_column='activation_code',
        null=True)
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

    def __unicode__(self):
        return "Profile for %s" % self.user.username


def create_new_user(first_name, last_name, password, email):
    auth = IonAuth()
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=email,
        is_staff=False,
        is_active=False
    )
    user.set_password(password),
    user.save()
    profile = Profile.objects.create(
        user=user,
        activCode=auth.generate_code()
    )


def notify_new_user(user, code):
    send_templated_email(
        [user], 'emails/registration_confirm',
        {'user': user, 'site_url': self.request.META['SERVER_NAME'],
         'activation_code': code, }
    )

