# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_flags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='forgotCode',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='forgotten_time',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='rememberCode',
        ),
    ]
