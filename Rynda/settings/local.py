# coding: utf-8

from .base import *

DEBUG = True
TEMPLATE_DEBUG = False
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


INSTALLED_APPS += (
    'debug_toolbar',
    'test',
)

INTERNAL_IPS = ('127.0.0.1')
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

