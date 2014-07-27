# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Subdomain'
        db.delete_table(u'core_subdomain')


    def backwards(self, orm):
        # Adding model 'Subdomain'
        db.create_table(u'core_subdomain', (
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('isCurrent', self.gf('django.db.models.fields.BooleanField')(db_column='is_current')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('disclaimer', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['Subdomain'])


    models = {
        u'core.infopage': {
            'Meta': {'object_name': 'Infopage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'db_column': "'text'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'title'"})
        }
    }

    complete_apps = ['core']