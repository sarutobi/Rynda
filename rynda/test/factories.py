# -*- coding: utf-8 -*-

import factory
from factory import django

from django.contrib.auth.models import User

from rynda.users.models import Profile


class ProfileFactory(django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory('test.factories.UserFactory', profile=None)


class UserFactory(django.DjangoModelFactory):
    FACTORY_FOR = User

    first_name = "Boy"
    last_name = factory.Sequence(lambda n: "Factory_%s" % n)
    email = factory.LazyAttribute(
        lambda a:
        "{0}_{1}@mail.ru".format(a.first_name, a.last_name).lower())
    username = factory.Sequence(lambda n: "username_%s" % n)
    password = factory.PostGenerationMethodCall('set_password', '123')
    is_active = True
    is_staff = False
    is_superuser = False

    profile = factory.RelatedFactory(ProfileFactory, 'user')
