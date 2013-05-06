# coding: utf-8

import factory

from django.contrib.auth.models import User


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    first_name = "Boy"
    last_name = factory.Sequence(lambda n: "Factory_%s" % n)
    email = factory.LazyAttribute(
        lambda a:
        "{0}_{1}@mail.ru".format(a.first_name, a.last_name).lower())
    username = factory.Sequence(lambda n: "username_%s" % n)
    password = '123'
    is_active = False
    is_staff = False
    is_superuser = False

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop("password", None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
        if create:
            user.save()
        return user
