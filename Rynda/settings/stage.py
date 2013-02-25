# coding: utf-8

import os
from .base import *

DEBUG = True

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

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(SITE_ROOT, 'mailbox')
