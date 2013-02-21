# coding: utf-8

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
TEST_DISCOVER_ROOT = SITE_ROOT
SOUTH_TESTS_MIGRATE = False
