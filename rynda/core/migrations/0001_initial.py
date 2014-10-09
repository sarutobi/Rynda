# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSocialLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('help_title', models.CharField(max_length=100, verbose_name='Help title')),
                ('url', models.CharField(max_length=2000, verbose_name='Link url')),
                ('ordering', models.IntegerField(verbose_name='Ordering')),
                ('site', models.ForeignKey(verbose_name='Site name', to='sites.Site')),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name': 'Social link',
                'verbose_name_plural': 'Social links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialLinkType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('symbol', models.CharField(max_length=200, verbose_name='Symbol', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sitesociallinks',
            name='social_link_type',
            field=models.ForeignKey(verbose_name='Link type', to='core.SocialLinkType'),
            preserve_default=True,
        ),
    ]
