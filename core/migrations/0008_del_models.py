# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (('category', '0001_add_models'), )

    def forwards(self, orm):
        pass

    def backwards(self, orm):
        pass


