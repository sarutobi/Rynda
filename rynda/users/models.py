# -*- coding: utf-8 -*-

import random
import base64
import hashlib
import string

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from post_office import mail


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
        salt = auth_code[:self.salt_len]
        digest = auth_code[self.salt_len:]

        # CAVEAT: Make sure UserAuthCode cannot be used to reactivate locked
        # profiles.
        if user.last_login >= user.date_joined:
            return False

        return digest == self.digest(user, salt)


class Profile(models.Model):
    """
    User profile
    """
    class Meta:
        ordering = ['user']
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    MALE, FEMALE, UNKNOWN = (1, 2, 0)
    SEX_CHOICES = (
        (UNKNOWN, _("Unknown")),
        (MALE, _("Male")),
        (FEMALE, _("Female")),
    )

    user = models.OneToOneField(User)
    is_public = models.BooleanField(_("Public"), default=False)
    phones = models.CharField(max_length=255, blank=True)
    about_me = models.TextField(default='', blank=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.IntegerField(_("Gender"), choices=SEX_CHOICES, default=UNKNOWN)

    def __unicode__(self):
        return "Profile for %s" % self.user.username


def create_new_user(first_name, last_name, password, email):
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
    Profile.objects.create(user=user)
    notify_new_user(user)
    return user


def notify_new_user(user):
    """ Send to new user activation link """

    activation_code = UserAuthCode(settings.SECRET_KEY).auth_code(user)
    mail.send(
        [user.email],
        template="registration confirmation",
        context={
            'user': user,
            'activation_code': activation_code,
            'site': Site.objects.get()
        }
    )


def activate_user(user, code):
    """ Checks activation code, activate user and send email notification """

    encoder = UserAuthCode(settings.SECRET_KEY)
    if encoder.is_valid(user, code):
        user.is_active = True
        user.save()
        mail.send(
            [user.email],
            template="registration complete",
            context={
                'user': user,
                'site': Site.objects.get(),
            }
        )
        return True
    return False
