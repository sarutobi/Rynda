# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table('groups', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column='id')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, db_column='name')),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='description')),
        ))
        db.send_create_signal('users', ['Group'])

        # Adding model 'Users'
        db.create_table('users', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column='id')),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('groupId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Group'], db_column='group_id')),
            ('ipAddr', self.gf('django.db.models.fields.CharField')(max_length=16, db_column='ip_address')),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=15, db_column='username')),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=40, db_column='password')),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, db_column='salt')),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100, db_column='email')),
            ('activCode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, db_column='activation_code')),
            ('forgotCode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, db_column='forgotten_password_code')),
            ('rememberCode', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, db_column='remember_code')),
            ('created', self.gf('django.db.models.fields.IntegerField')(db_column='created_on')),
            ('lastLogin', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='last_login')),
            ('active', self.gf('django.db.models.fields.NullBooleanField')(null=True, db_column='active', blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50, db_column='first_name')),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, db_column='last_name')),
            ('forgotten_time', self.gf('django.db.models.fields.IntegerField')(db_column='forgotten_password_time')),
            ('ref_type', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='ref_type')),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='flags')),
            ('phones', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')()),
            ('my_photo', self.gf('django.db.models.fields.IntegerField')()),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('gender', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('users', ['Users'])

        # Adding model 'MetaUser'
        db.create_table('meta', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column='id')),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.Users'], unique=True, db_column='user_id')),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=50, db_column='first_name')),
            ('lastName', self.gf('django.db.models.fields.CharField')(max_length=50, db_column='last_name')),
            ('flags', self.gf('django.db.models.fields.IntegerField')(db_column='flags')),
        ))
        db.send_create_signal('users', ['MetaUser'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table('groups')

        # Deleting model 'Users'
        db.delete_table('users')

        # Deleting model 'MetaUser'
        db.delete_table('meta')


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
        'users.group': {
            'Meta': {'ordering': "['id']", 'object_name': 'Group', 'db_table': "'groups'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'description'"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_column': "'name'"})
        },
        'users.metauser': {
            'Meta': {'object_name': 'MetaUser', 'db_table': "'meta'"},
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'first_name'"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'db_column': "'flags'"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'last_name'"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['users.Users']", 'unique': 'True', 'db_column': "'user_id'"})
        },
        'users.users': {
            'Meta': {'ordering': "['created']", 'object_name': 'Users', 'db_table': "'users'"},
            'about_me': ('django.db.models.fields.TextField', [], {}),
            'activCode': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'db_column': "'activation_code'"}),
            'active': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'active'", 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'created': ('django.db.models.fields.IntegerField', [], {'db_column': "'created_on'"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'db_column': "'email'"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'first_name'"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'flags'"}),
            'forgotCode': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'db_column': "'forgotten_password_code'"}),
            'forgotten_time': ('django.db.models.fields.IntegerField', [], {'db_column': "'forgotten_password_time'"}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'groupId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Group']", 'db_column': "'group_id'"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'ipAddr': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_column': "'ip_address'"}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'lastLogin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'last_login'"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'last_name'"}),
            'my_photo': ('django.db.models.fields.IntegerField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_column': "'password'"}),
            'phones': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ref_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'ref_type'"}),
            'rememberCode': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'db_column': "'remember_code'"}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'db_column': "'salt'"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_column': "'username'"})
        }
    }

    complete_apps = ['users']