# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'core_category')

        # Deleting model 'CategoryGroup'
        db.delete_table(u'core_categorygroup')


    def backwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'core_category', (
            ('subdomain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subdomain'], null=True, db_column='subdomain_id', blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, db_column='slug', blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CategoryGroup'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(db_column='description', blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='name')),
            ('color', self.gf('django.db.models.fields.CharField')(default='#000000', max_length=7, db_column='color')),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(db_column='order')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='icon', blank=True)),
        ))
        db.send_create_signal('core', ['Category'])

        # Adding model 'CategoryGroup'
        db.create_table(u'core_categorygroup', (
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['CategoryGroup'])


    models = {
        u'core.infopage': {
            'Meta': {'object_name': 'Infopage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'db_column': "'text'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'title'"})
        },
        u'core.subdomain': {
            'Meta': {'ordering': "['order']", 'object_name': 'Subdomain'},
            'disclaimer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCurrent': ('django.db.models.fields.BooleanField', [], {'db_column': "'is_current'"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']