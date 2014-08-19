# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table(u'geozones_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
            ('zoom', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'geozones', ['Region'])

        # Adding model 'Location'
        db.create_table(u'geozones_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Location', max_length=250)),
            ('coordinates', self.gf('django.contrib.gis.db.models.fields.GeometryCollectionField')(null=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geozones.Region'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'geozones', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Region'
        db.delete_table(u'geozones_region')

        # Deleting model 'Location'
        db.delete_table(u'geozones_location')


    models = {
        u'geozones.location': {
            'Meta': {'object_name': 'Location'},
            'coordinates': ('django.contrib.gis.db.models.fields.GeometryCollectionField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Location'", 'max_length': '250'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geozones.Region']", 'null': 'True', 'blank': 'True'})
        },
        u'geozones.region': {
            'Meta': {'ordering': "['order']", 'object_name': 'Region'},
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'zoom': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['geozones']