# coding: utf-8

import factory

from factory import django
from factory.fuzzy import BaseFuzzyAttribute

import random

from .models import Location, Region


class FuzzyPoint(BaseFuzzyAttribute):
    """ Generate fuzzy geojango point """
    def fuzz(self):
        lat = random.uniform(-90.0, 90.0)
        lon = random.uniform(-180.0, 180.0)
        return "POINT(%f %f)" % (lon, lat)


class FuzzyPoints(BaseFuzzyAttribute):
    """ Generate list of geodjango points """
    def fuzz(self):
        lat = random.uniform(-90.0, 90.0)
        lon = random.uniform(-180.0, 180.0)
        return "GEOMETRYCOLLECTION(POINT(%f %f))" % (lon, lat)


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
    coordinates = FuzzyPoints()
    description = factory.Sequence(lambda n: "Location_%s" % n)
    region = factory.SubFactory(RegionFactory)
