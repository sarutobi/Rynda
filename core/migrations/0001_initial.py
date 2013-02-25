# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subdomain'
        db.create_table('core_subdomain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('isCurrent', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='is_current')),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('disclaimer', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('core', ['Subdomain'])

        # Adding model 'Category'
        db.create_table('core_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parentId', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent', db_column='parent_id', default=0, to=orm['core.Category'], blank=True, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='name')),
            ('description', self.gf('django.db.models.fields.TextField')(db_column='description', blank=True)),
            ('color', self.gf('django.db.models.fields.CharField')(default='#000000', max_length=7, db_column='color')),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, db_column='slug', blank=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='icon', blank=True)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(db_column='order')),
            ('subdomain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subdomain'], null=True, db_column='subdomain_id', blank=True)),
            ('group', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Category'])

        # Adding model 'Infopage'
        db.create_table('core_infopage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='title')),
            ('text', self.gf('django.db.models.fields.TextField')(db_column='text')),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal('core', ['Infopage'])


    def backwards(self, orm):
        # Deleting model 'Subdomain'
        db.delete_table('core_subdomain')

        # Deleting model 'Category'
        db.delete_table('core_category')

        # Deleting model 'Infopage'
        db.delete_table('core_infopage')


    models = {
        'core.category': {
            'Meta': {'ordering': "['order']", 'object_name': 'Category'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'#000000'", 'max_length': '7', 'db_column': "'color'"}),
            'description': ('django.db.models.fields.TextField', [], {'db_column': "'description'", 'blank': 'True'}),
            'group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'icon'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'name'"}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'db_column': "'order'"}),
            'parentId': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent'", 'db_column': "'parent_id'", 'default': '0', 'to': "orm['core.Category']", 'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_column': "'slug'", 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Subdomain']", 'null': 'True', 'db_column': "'subdomain_id'", 'blank': 'True'})
        },
        'core.infopage': {
            'Meta': {'object_name': 'Infopage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'db_column': "'text'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'title'"})
        },
        'core.subdomain': {
            'Meta': {'ordering': "['order']", 'object_name': 'Subdomain'},
            'disclaimer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCurrent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_current'"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']