# coding: utf-8

from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'devrynda',
        'USER': 'devrynda',
        'PASSWORD': 'devrynda',
        'HOST': 'localhost',
        'PORT': '',
    }
}

SOUTH_TESTS_MIGRATE = False

try:
    from local_test import *
except:
    pass
