# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_auto_20141214_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='linked_location',
        ),
    ]
