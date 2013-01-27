# -*- coding: utf-8 -*-

import hashlib
import time
from random import random

from django.contrib.auth.models import User


class IonAuth(object):
    '''
    Authentication against the codeigniter "ion auth" library
    '''
    SALT_LENGTH = 10

    def get_user(self, user_id):
        '''
        Backend implementation
        '''
        try:
            return User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return None

    def authenticate(self, username=None, password=None):
        '''
        Backend implementation.
        Implement the ion auth validation algorytm
        '''
        if not username or not password:
            return None
        try:
            user = User.objects.get(email=username)
        except Exception:
            return None
        if not user.is_active:
            return None
        check = self.password_hash(password,
            salt=user.password[:self.SALT_LENGTH])
        if user.password != check:
            return None
        #Rehash user password to standart Django 
        user.set_password(password)
        user.save()
        return user

    def gen_salt(self):
        '''
        Generate password salt, similar to ion auth.
        '''
        hasher = hashlib.md5()
        hasher.update("%f" % random())
        hasher.update("%d" %time.time())
        return hasher.hexdigest()[:self.SALT_LENGTH]

    def password_hash(self, password, salt=None):
        '''
        Hashes plain password by ion auth algorythm
        '''
        if salt is None:
            salt = self.gen_salt()
        hasher = hashlib.sha1()
        hasher.update(salt)
        hasher.update(password)
        return "%s%s" % (salt, hasher.hexdigest()[:-self.SALT_LENGTH])

    def generate_code(self):
        '''
        Generate activation or frogot password code
        '''
        hasher = hashlib.sha1()
        hasher.update(self.gen_salt())
        s = hasher.digest()
        hasher.update('%s%s%s' %(s, self.gen_salt(), s))
        return hasher.hexdigest()
