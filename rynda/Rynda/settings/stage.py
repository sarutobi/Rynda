# coding: utf-8

from .base import *

DEBUG = TEMPLATE_DEBUG = True

EXTERNAL = True

try:
    from local_stage import *
except:
    pass
