# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forgotCode', models.CharField(max_length=40, null=True, editable=False, db_column='forgotten_password_code')),
                ('rememberCode', models.CharField(max_length=40, null=True, editable=False, db_column='remember_code')),
                ('forgotten_time', models.DateTimeField(null=True, editable=False, db_column='forgotten_password_time')),
                ('flags', models.IntegerField(default=0, editable=False, db_column='flags')),
                ('phones', models.CharField(max_length=255, blank=True)),
                ('about_me', models.TextField(default='', blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('gender', models.IntegerField(default=0, verbose_name='Gender', choices=[(0, 'Unknown'), (1, 'Male'), (2, 'Female')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
            ],
            options={
                'ordering': ['user'],
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
            bases=(models.Model,),
        ),
    ]
