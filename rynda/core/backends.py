# -*- coding: utf-8 -*-

import hashlib
import time
from random import random

from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class IonAuth(object):
    """ Authentication against the codeigniter "ion auth" library """

    supports_inactive_user = False
    SALT_LENGTH = 10

    def get_user(self, user_id):
        """ Backend implementation """

        try:
            return User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return None

    def authenticate(self, username=None, password=None):
        """
        Backend implementation.

        Implement the ion auth validation algorytm
        """
        if not username or not password:
            return None
        try:
            user = User.objects.get(email=username)
        except Exception:
            return None
        if not user.is_active:
            return None
        check = self.password_hash(
            password,
            salt=user.password[:self.SALT_LENGTH])
        if user.password != check:
            return None
        # Rehash user password to standart Django
        user.set_password(password)
        user.save()
        return user

    def gen_salt(self):
        """ Generate password salt, similar to ion auth.  """

        hasher = hashlib.md5()
        hasher.update("%f".encode() % random())
        hasher.update("%d".encode() % time.time())
        return hasher.hexdigest()[:self.SALT_LENGTH]

    def password_hash(self, password, salt=None):
        """ Hashes plain password by ion auth algorythm """

        if salt is None:
            salt = self.gen_salt()
        hasher = hashlib.sha1()
        hasher.update(salt.encode())
        if isinstance(password, str):
            hasher.update(password.encode())
        else:
            hasher.update(password)
        return "%s%s" % (salt, hasher.hexdigest()[:-self.SALT_LENGTH])
