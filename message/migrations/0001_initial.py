# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MessageType'
        db.create_table('message_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('message', ['MessageType'])

        # Adding model 'Message'
        db.create_table('message_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('sender', self.gf('django.db.models.fields.TextField')()),
            ('contact_first_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('contact_last_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('contact_mail', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('messageType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['message.MessageType'], db_column='message_type')),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('flags', self.gf('django.db.models.fields.BigIntegerField')()),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_column='date_add', blank=True)),
            ('last_edit', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_column='date_modify', blank=True)),
            ('expired_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='user_id', blank=True)),
            ('edit_key', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Location'], null=True, db_column='location_id')),
            ('subdomain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subdomain'], null=True, db_column='subdomain_id', blank=True)),
        ))
        db.send_create_signal('message', ['Message'])

        # Adding M2M table for field category on 'Message'
        db.create_table('messagecategories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm['message.message'], null=False)),
            ('category', models.ForeignKey(orm['core.category'], null=False))
        ))
        db.create_unique('messagecategories', ['message_id', 'category_id'])

        # Adding model 'MessageNotes'
        db.create_table('message_messagenotes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['message.Message'])),
            ('user', self.gf('django.db.models.fields.IntegerField')()),
            ('note', self.gf('django.db.models.fields.TextField')()),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_edit', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('message', ['MessageNotes'])


    def backwards(self, orm):
        # Deleting model 'MessageType'
        db.delete_table('message_type')

        # Deleting model 'Message'
        db.delete_table('message_message')

        # Removing M2M table for field category on 'Message'
        db.delete_table('messagecategories')

        # Deleting model 'MessageNotes'
        db.delete_table('message_messagenotes')


    models = {
        'core.category': {
            'Meta': {'ordering': "['order']", 'object_name': 'Category', 'db_table': "'Category'"},
            'color': ('django.db.models.fields.CharField', [], {'default': "'#000000'", 'max_length': '7', 'db_column': "'color'"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'description'"}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'icon'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'name'"}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'db_column': "'order'"}),
            'parentId': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent'", 'db_column': "'parent_id'", 'default': '0', 'to': "orm['core.Category']", 'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_column': "'slug'", 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Subdomain']", 'null': 'True', 'db_column': "'subdomain_id'", 'blank': 'True'})
        },
        'core.city': {
            'Meta': {'object_name': 'City', 'db_table': "'City'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longtitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'region_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Region']", 'db_column': "'region_id'"})
        },
        'core.location': {
            'Meta': {'object_name': 'Location', 'db_table': "'Location'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {'db_column': "'longitude'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'regionId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Region']", 'db_column': "'region_id'"})
        },
        'core.region': {
            'Meta': {'ordering': "['order']", 'object_name': 'Region', 'db_table': "'Region'"},
            'cityId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.City']", 'db_column': "'city_id'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'zoomLvl': ('django.db.models.fields.SmallIntegerField', [], {'db_column': "'zoom_lvl'"})
        },
        'core.subdomain': {
            'Meta': {'ordering': "['order']", 'object_name': 'Subdomain', 'db_table': "'subdomain'"},
            'disclaimer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCurrent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_current'"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'message.message': {
            'Meta': {'ordering': "['-date_add']", 'object_name': 'Message'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Category']", 'db_table': "'messagecategories'", 'symmetrical': 'False'}),
            'contact_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contact_last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contact_mail': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_column': "'date_add'", 'blank': 'True'}),
            'edit_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'expired_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'flags': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_column': "'date_modify'", 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Location']", 'null': 'True', 'db_column': "'location_id'"}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'messageType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message.MessageType']", 'db_column': "'message_type'"}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'sender': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'subdomain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Subdomain']", 'null': 'True', 'db_column': "'subdomain_id'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'user': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'user_id'", 'blank': 'True'})
        },
        'message.messagenotes': {
            'Meta': {'object_name': 'MessageNotes'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message.Message']"}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.IntegerField', [], {})
        },
        'message.messagetype': {
            'Meta': {'object_name': 'MessageType', 'db_table': "'message_type'"},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['message']