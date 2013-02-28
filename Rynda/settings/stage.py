# coding: utf-8

import os

from .base import *

DEBUG = TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'devrynda',
        'USER': 'devrynda',
        'PASSWORD': 'RyndaDeveloper',
        'HOST': 'rynda.org',
        'PORT': '',
    }
}
STATIC_ROOT = os.path.join(get_env_var('STATIC_ROOT'), 'rynda', 'static')
