# coding: utf-8

import factory

from factory import django
import random

from .models import Location, Region


class RegionFactory(django.DjangoModelFactory):
    FACTORY_FOR = Region

    name = factory.Sequence(lambda n: "Region_%s" % n)
    slug = factory.LazyAttribute(lambda a: a.name.lower())
    latitude = random.uniform(-90.0, 90.0)
    longitude = random.uniform(-180.0, 180.0)
    zoom = random.randint(1, 10)
    order = factory.Sequence(lambda n: n)


class LocationFactory(django.DjangoModelFactory):
    FACTORY_FOR = Location

    latitude = random.uniform(-90.0, 90.0)
    longitude = random.uniform(-180.0, 180.0)
    description = factory.Sequence(lambda n: "Location_%s" % n)
    region = factory.SubFactory(RegionFactory)
