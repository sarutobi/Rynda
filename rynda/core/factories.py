# coding: utf-8

import factory
import random

from factory import django, fuzzy
from django.contrib.gis.geos import fromstr, Point, MultiPoint, GeometryCollection

from rynda.message.models import Category


class FuzzyPoint(fuzzy.BaseFuzzyAttribute):
    """ Generate fuzzy geojango point """
    def point_gen(self):
        lat = random.uniform(-90.0, 90.0)
        lon = random.uniform(-180.0, 180.0)
        return Point(lat, lon)

    def fuzz(self):
        return self.point_gen().wkt


class FuzzyMultiPoint(fuzzy.BaseFuzzyAttribute):
    def fuzz(self):
        p1 = FuzzyPoint().point_gen()
        p2 = FuzzyPoint().point_gen()
        mp = MultiPoint(p1, p2)
        return mp.wkt


class FuzzyGeometryCollection(fuzzy.BaseFuzzyAttribute):
    def fuzz(self):
        p1 = FuzzyPoint().point_gen()
        p2 = FuzzyPoint().point_gen()
        return GeometryCollection(p1, p2).wkt


class CategoryFactory(django.DjangoModelFactory):
    FACTORY_FOR = Category

    name = factory.Sequence(lambda n: "Category %s" % n)
    order = factory.Sequence(lambda n: n)
