# -*- coding: utf-8 -*-

import random
import base64
import hashlib
import string

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from post_office import mail


class UserAuthCode(object):
    def __init__(self, secret, salt_len=8, hash=hashlib.sha256):
        self.secret = secret
        self.salt_len = salt_len
        s = [random.choice(string.ascii_letters + string.digits)
             for i in range(self.salt_len)]
        self._salt = "".join(s)
        self.hash = hash

    def salt(self):
        return self._salt

    def digest(self, user):
        # Use username, email and date_joined to generate digest
        auth_message = "".join((self.secret, user.username, user.email,
                               str(user.date_joined), self._salt))
        md = self.hash()
        md.update(auth_message.encode('utf8'))

        return base64.urlsafe_b64encode(md.digest()).rstrip(b'=').decode()

    def auth_code(self, user):
        salt = self.salt()
        digest = self.digest(user)

        return "%s%s" % (self._salt, digest)

    def is_valid(self, user, auth_code):
        salt = auth_code[:self.salt_len]
        digest = auth_code[self.salt_len:]

        # CAVEAT: Make sure UserAuthCode cannot be used to reactivate locked
        # profiles.
        if user.last_login is not None and user.last_login >= user.date_joined:
            return False
        s = self._salt
        self._salt = salt
        digest_check = self.digest(user)
        self._salt = s
        return digest == digest_check


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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    notify_new_user(user)
    return user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


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


def list_public_users():
    """ Returns query for select only active users with public profile flag """
    return User.objects.select_related().filter(is_active=True, profile__is_public=True)
