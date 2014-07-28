# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import signals

from users import models as users_app


def create_anonymous_user(sender, **kwargs):
    User = get_user_model()
    ANONYMOUS_USER_ID = settings.ANONYMOUS_USER_ID
    ANONYMOUS_DEFAULT_USERNAME = getattr(
        settings, "ANONYMOUS_DEFAULT_USERNAME", "anonymous")
    try:
        User.objects.get(pk=ANONYMOUS_USER_ID)
    except User.DoesNotExist:
        User.objects.create(
            pk=ANONYMOUS_USER_ID,
            **{User.USERNAME_FIELD: ANONYMOUS_DEFAULT_USERNAME})

if hasattr(settings, "ANONYMOUS_USER_ID"):
    signals.post_syncdb.connect(
        create_anonymous_user, sender=users_app,
        dispatch_uid="users.management.create_anonymous_user")
