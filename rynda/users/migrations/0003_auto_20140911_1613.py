# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_public_flags(apps, schema_editor):
    Profile = apps.get_model("users", "Profile")
    for profile in Profile.objects.all():
        profile.is_public = 1 == (profile.flags & 1)
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_is_public'),
    ]

    operations = [
        migrations.RunPython(set_public_flags)
    ]
