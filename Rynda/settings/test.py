# coding: utf-8

from .local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_ROOT = os.path.join(SITE_ROOT, 'test')
SOUTH_TESTS_MIGRATE = False
