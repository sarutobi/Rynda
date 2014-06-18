# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Location.longitude'
        db.delete_column(u'geozones_location', 'longitude')

        # Deleting field 'Location.latitude'
        db.delete_column(u'geozones_location', 'latitude')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Location.longitude'
        raise RuntimeError("Cannot reverse this migration. 'Location.longitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Location.longitude'
        db.add_column(u'geozones_location', 'longitude',
                      self.gf('django.db.models.fields.FloatField')(db_column='longitude'),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Location.latitude'
        raise RuntimeError("Cannot reverse this migration. 'Location.latitude' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Location.latitude'
        db.add_column(u'geozones_location', 'latitude',
                      self.gf('django.db.models.fields.FloatField')(),
                      keep_default=False)


    models = {
        u'geozones.location': {
            'Meta': {'object_name': 'Location'},
            'coordinates': ('django.contrib.gis.db.models.fields.GeometryCollectionField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Location'", 'max_length': '250'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geozones.Region']"})
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