# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='message',
            name='messageType',
            field=models.IntegerField(verbose_name='Message type', db_column=b'message_type', choices=[(1, 'Request message'), (2, 'Offer message')]),
        ),
        migrations.AlterField(
            model_name='message',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title', blank=True),
        ),
    ]
