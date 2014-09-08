# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geozones', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name', db_column=b'name')),
                ('description', models.TextField(verbose_name='description', db_column=b'description', blank=True)),
                ('slug', models.SlugField(max_length=255, verbose_name='slug', db_column=b'slug', blank=True)),
                ('order', models.SmallIntegerField(db_column=b'order')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title', blank=True)),
                ('message', models.TextField(verbose_name='Message')),
                ('additional_info', jsonfield.fields.JSONField(default=b'', verbose_name='Additional info', blank=True)),
                ('messageType', models.IntegerField(verbose_name='Message type', db_column=b'message_type', choices=[(1, 'Request message'), (2, 'Offer message'), (3, 'Informatial message')])),
                ('source', models.CharField(max_length=255, verbose_name='source', blank=True)),
                ('is_virtual', models.BooleanField(default=False, verbose_name='Is virtual')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_important', models.BooleanField(default=False, verbose_name='important')),
                ('is_anonymous', models.BooleanField(default=True, verbose_name='hide contacts')),
                ('is_removed', models.BooleanField(default=False, verbose_name='removed')),
                ('allow_feedback', models.BooleanField(default=True, verbose_name='allow feedback')),
                ('status', models.SmallIntegerField(default=1, null=True, verbose_name='status', blank=True, choices=[(1, 'New'), (2, 'Unverified'), (3, 'Verified'), (4, 'Pending'), (6, 'Closed')])),
                ('date_add', models.DateTimeField(auto_now_add=True, db_column=b'date_add')),
                ('last_edit', models.DateTimeField(auto_now=True, db_column=b'date_modify')),
                ('expired_date', models.DateTimeField(null=True, verbose_name='expired at', blank=True)),
                ('edit_key', models.CharField(max_length=40, blank=True)),
                ('sender_ip', models.IPAddressField(verbose_name='sender IP', null=True, editable=False, blank=True)),
                ('category', models.ManyToManyField(to='message.Category', null=True, verbose_name='message categories', blank=True)),
                ('linked_location', models.ForeignKey(blank=True, to='geozones.Location', null=True)),
                ('user', models.ForeignKey(db_column=b'user_id', editable=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['-date_add'],
                'get_latest_by': 'date_add',
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageNotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(verbose_name='Note')),
                ('date_add', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('last_edit', models.DateTimeField(auto_now=True, verbose_name='Last edit')),
                ('message', models.ForeignKey(to='message.Message')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
