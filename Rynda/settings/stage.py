# coding: utf-8

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

INSTALLED_APPS += (
    'django_unicorn',
)
