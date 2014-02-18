# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Move model 'Category'
        db.rename_table(u'core_category', u'category_category')
        # Move model 'CategoryGroup'
        db.rename_table(u'core_categorygroup', u'category_categorygroup')
        if not db.dry_run:
            # For permissions to work properly after migrating
            orm['contenttypes.contenttype'].objects.filter(app_label='core', model='category').update(app_label='category')

    def backwards(self, orm):
        # Move model 'Category'
        db.rename_table(u'category_category, 'u'core_category')
        # Move model 'CategoryGroup'
        db.rename_table(u'category_categorygroup', u'core_categorygroup')
        if not db.dry_run:
            # For permissions to work properly after migrating
            orm['contenttypes.contenttype'].objects.filter(app_label='category', model='category').update(app_label='core')

    # Deleting model 'Category'
        db.delete_table(u'category_category')

        # Deleting model 'CategoryGroup'
        db.delete_table(u'category_categorygroup')


        complete_apps = ['category']
