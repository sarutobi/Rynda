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

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['category', 'contenttypes']
