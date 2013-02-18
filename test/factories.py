# coding: utf-8

import factory

from django.contrib.auth.models import User


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    first_name = "Boy"
    last_name = "Factory"
    email = factory.LazyAttribute(
        lambda a:
        "{0}_{1}@example.com".format(a.first_name, a.last_name).lower())
    username = factory.Sequence(lambda n: "username_%s" % n)
    is_active = False
    is_staff = False
    is_superuser = False
