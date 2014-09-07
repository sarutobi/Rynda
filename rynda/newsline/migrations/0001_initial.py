# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('post', models.TextField(verbose_name='Post')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publish')),
                ('status', models.IntegerField(verbose_name='Status', choices=[(0, 'draft'), (1, 'published')])),
                ('author', models.ForeignKey(verbose_name='Author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-publish'],
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
            bases=(models.Model,),
        ),
    ]
