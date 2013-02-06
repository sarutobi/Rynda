# coding: utf-8

from .base import *

DEBUG = TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
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

