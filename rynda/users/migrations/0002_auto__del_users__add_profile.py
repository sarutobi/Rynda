# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Users'
        db.delete_table('users_users')

        # Adding model 'Profile'
        db.create_table('users_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('activCode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, db_column='activation_code')),
            ('forgotCode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, db_column='forgotten_password_code')),
            ('rememberCode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, db_column='remember_code')),
            ('forgotten_time', self.gf('django.db.models.fields.DateTimeField')(null=True, db_column='forgotten_password_time')),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='flags')),
            ('phones', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')(default='')),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('users', ['Profile'])


    def backwards(self, orm):
        # Adding model 'Users'
        db.create_table('users_users', (
            ('phones', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('rememberCode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, db_column='remember_code')),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')(default='')),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('forgotten_time', self.gf('django.db.models.fields.DateTimeField')(null=True, db_column='forgotten_password_time')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forgotCode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, db_column='forgotten_password_code')),
            ('gender', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='flags')),
            ('activCode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, db_column='activation_code')),
        ))
        db.send_create_signal('users', ['Users'])

        # Deleting model 'Profile'
        db.delete_table('users_profile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.profile': {
            'Meta': {'ordering': "['user']", 'object_name': 'Profile'},
            'about_me': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'activCode': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'db_column': "'activation_code'"}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'flags'"}),
            'forgotCode': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'db_column': "'forgotten_password_code'"}),
            'forgotten_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'forgotten_password_time'"}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phones': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rememberCode': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'db_column': "'remember_code'"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['users']