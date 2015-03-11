# coding: utf-8

from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': 'rynda.db',
    }
}

LANGUAGE_CODE = 'en'

try:
    from local_test import *
except:
    pass
