# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models, connection

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        sql = '''insert into message_message (id, title, message, date_add, date_modify, subdomain_id, location_id, user_id,
        contact_first_name, contact_last_name, contact_phone, contact_mail, flags, message_type, status
        )
        SELECT id, title, message,date_add, date_modify, subdomain_id, location_id, user_id,
        (xpath('/sender/firstname/text()[1]'::text, sender))[1]::character varying(100) AS sender_first_name,
        (xpath('/sender/lastname/text()[1]'::text, sender))[1]::character varying(100) AS sender_last_name,
        --(xpath('/sender/patrname/text()[1]'::text, sender))[1]::character varying(100) AS sender_patr_name,
        array_to_string(xpath('/sender/phone/text()'::text, sender)::character varying(12)[], ',')  AS sender_phone,
        (xpath('/sender/email/text()[1]'::text, sender))[1]::character varying(100) AS sender_email,
        flags, message_type, status FROM "Message"'''
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.execute('''select setval('message_message_id_seq', (select max(id) from message_message))''')
    def backwards(self, orm):
        "Write your backwards methods here."

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
            'sender_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
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
    symmetrical = True
