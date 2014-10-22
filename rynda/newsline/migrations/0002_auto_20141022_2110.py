# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('newsline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Published'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(verbose_name='status', choices=[(0, 'draft'), (1, 'Published')]),
        ),
    ]
