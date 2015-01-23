# coding: utf-8

import factory
import random

from factory import django

from rynda.core.factories import FuzzyPoint
from .models import Region


class RegionFactory(django.DjangoModelFactory):
    FACTORY_FOR = Region

    name = factory.Sequence(lambda n: "Region_%s" % n)
    slug = factory.LazyAttribute(lambda a: a.name.lower())
    center = FuzzyPoint()
    zoom = random.randint(1, 10)
    order = factory.Sequence(lambda n: n)
