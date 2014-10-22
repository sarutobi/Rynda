# coding: utf-8

import factory
import random

from factory import django

from rynda.core.factories import FuzzyPoint, FuzzyGeometryCollection
from .models import Location, Region


class RegionFactory(django.DjangoModelFactory):
    FACTORY_FOR = Region

    name = factory.Sequence(lambda n: "Region_%s" % n)
    slug = factory.LazyAttribute(lambda a: a.name.lower())
    center = FuzzyPoint()
    zoom = random.randint(1, 10)
    order = factory.Sequence(lambda n: n)


class LocationFactory(django.DjangoModelFactory):
    FACTORY_FOR = Location

    name = factory.Sequence(lambda n: "Item %s" % n)
    coordinates = FuzzyGeometryCollection()
    description = factory.Sequence(lambda n: "Location_%s" % n)
    region = factory.SubFactory(RegionFactory)
