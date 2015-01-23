# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_auto_20141022_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='address',
            field=models.CharField(default='', max_length=250, verbose_name='Address', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='location',
            field=django.contrib.gis.db.models.fields.MultiPointField(srid=4326, null=True, verbose_name='On map', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='messageType',
            field=models.IntegerField(verbose_name='Message type', db_column=b'message_type', choices=[(1, 'Help requests'), (2, 'Help offers')]),
        ),
    ]
