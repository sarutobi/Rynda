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

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (56.0, 45.0),
    'DEFAULT_ZOOM': 4,
    'MAX_ZOOM': 18,
    'MIN_ZOOM': 3,
    'RESET_VIEW': False,
}


def show_toolbar(request):
    uri = request.get_full_path()
    if re.match('/admin/', uri) or re.match('/api/', uri):
        return False
    return debug_toolbar.middleware.show_toolbar


INSTALLED_APPS += (
    'debug_toolbar',
    'test',
)

INTERNAL_IPS = ('127.0.0.1')
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': "rynda.Rynda.settings.local.show_toolbar",
}
