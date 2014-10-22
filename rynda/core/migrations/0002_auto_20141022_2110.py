# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitesociallinks',
            options={'ordering': ['ordering'], 'verbose_name': 'Site contact', 'verbose_name_plural': 'Site contacts'},
        ),
        migrations.AlterModelOptions(
            name='sociallinktype',
            options={'verbose_name': 'Contact type', 'verbose_name_plural': 'Contact types'},
        ),
        migrations.AlterField(
            model_name='sitesociallinks',
            name='help_title',
            field=models.CharField(max_length=100, verbose_name='Link title'),
        ),
        migrations.AlterField(
            model_name='sitesociallinks',
            name='url',
            field=models.CharField(help_text="Include protocol, ex. 'mailto:email@host' for email", max_length=2000, verbose_name='Link url'),
        ),
    ]
