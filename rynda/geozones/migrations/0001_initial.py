# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Location', max_length=250, verbose_name='Name')),
                ('coordinates', django.contrib.gis.db.models.fields.GeometryCollectionField(srid=4326, null=True, verbose_name='On map')),
                ('description', models.CharField(max_length=200, blank=True)),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Region name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, verbose_name='Map center')),
                ('zoom', models.SmallIntegerField(verbose_name='Map zoom')),
                ('order', models.IntegerField(verbose_name='Order')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.ForeignKey(verbose_name='Region', blank=True, to='geozones.Region', null=True),
            preserve_default=True,
        ),
    ]
