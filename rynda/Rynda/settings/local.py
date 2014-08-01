# coding: utf-8

import re
import debug_toolbar
from .base import *

DEBUG = True
TEMPLATE_DEBUG = True
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


def show_toolbar(request):
    uri = request.get_full_path()
    if re.match('/admin/', uri):
        return False
    return debug_toolbar.middleware.show_toolbar


INSTALLED_APPS += (
    'debug_toolbar',
    'test',
)

INTERNAL_IPS = ('127.0.0.1')
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': "Rynda.settings.local.show_toolbar",
}
