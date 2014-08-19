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

EXTERNAL = True
VK_APP_ID = get_env_var('vk_app_id')

try:
    from local_stage import *
except:
    pass
