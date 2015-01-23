# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('core', '0002_auto_20141022_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteMapOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zoom', models.SmallIntegerField(default=3, verbose_name='Map zoom')),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Default map center')),
                ('site', models.OneToOneField(verbose_name='Site name', to='sites.Site')),
            ],
            options={
                'verbose_name': 'Site map options',
            },
            bases=(models.Model,),
        ),
    ]
