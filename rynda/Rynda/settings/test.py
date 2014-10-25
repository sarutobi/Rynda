# coding: utf-8

from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': 'devrynda.db',
    }
}

try:
    from local_test import *
except:
    pass
