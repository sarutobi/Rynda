# -*- coding: utf-8 -*-

import hashlib

from django.contrib.auth.models import User
from users.models import Users

class IonAuth(object):
    '''
    Authentication against the codeigniter "ion auth" library
    '''

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, username=None, password=None):
        '''
        Implement the ion auth validation algorytm
        '''
        if not username or not password:
            return None
        try:
            u = Users.objects.get(email=username)
        except Exception:
            return None
        salt = u.password[:10]
        hasher = hashlib.sha1()
        hasher.update(salt)
        hasher.update(password)
        check = "%s%s" % (salt, hasher.hexdigest()[:-10])
        if u.password != check:
            return None
        return User.objects.get(id=u.id)

