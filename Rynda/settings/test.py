# coding: utf-8

import os

from .local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
TEST_RUNNER = 'discover_runner.DiscoverRunner'
#TEST_DISCOVER_TOP_LEVEL = os.path.join(SITE_ROOT, 'test')
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
SOUTH_TESTS_MIGRATE = False
