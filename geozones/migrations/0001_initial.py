# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table('geozones_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('zoom', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('geozones', ['Region'])

        # Adding model 'Location'
        db.create_table('geozones_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')(db_column='longitude')),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geozones.Region'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('geozones', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Region'
        db.delete_table('geozones_region')

        # Deleting model 'Location'
        db.delete_table('geozones_location')


    models = {
        'geozones.location': {
            'Meta': {'object_name': 'Location'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {'db_column': "'longitude'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geozones.Region']", 'null': 'True', 'blank': 'True'})
        },
        'geozones.region': {
            'Meta': {'ordering': "['order']", 'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'zoom': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['geozones']