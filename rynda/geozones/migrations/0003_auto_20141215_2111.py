# -*- coding: utf-8 -*-
#  from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_remove_message_linked_location'),
        ('geozones', '0002_auto_20141022_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='region',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
