# coding: utf-8

import factory
import random

from factory import django, fuzzy
from django.contrib.gis.geos import Point, MultiPoint, GeometryCollection

from test.utils import FuzzyText
from category.models import Category, CategoryGroup
from .models import Subdomain


class FuzzyPoint(fuzzy.BaseFuzzyAttribute):
    """ Generate fuzzy geojango point """
    def fuzz(self):
        lat = random.uniform(-90.0, 90.0)
        lon = random.uniform(-180.0, 180.0)
        return Point(lon, lat).wkt


class FuzzyMultiPoint(fuzzy.BaseFuzzyAttribute):
    def fuzz(self):
        p1 = Point(0, 1)
        p2 = Point(2, 4)
        mp = MultiPoint(p1, p2)
        return mp.wkt


class FuzzyGeometryCollection(fuzzy.BaseFuzzyAttribute):
    def fuzz(self):
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        return GeometryCollection(p1, p2).wkt


#class CityFactory(factory.Factory):
#    FACTORY_FOR = City
#
#    name = factory.Sequence(lambda n: "City_%s" % n)
#    latitude = random.uniform(-90.0, 90.0)
#    longtitude = random.uniform(-180.0, 180.0)
#    #region_id = factory.Sequence(lambda n: n)


class CategoryGroupFactory(django.DjangoModelFactory):
    FACTORY_FOR = CategoryGroup

    name = factory.Sequence(lambda n: "Category group %s" % n)
    order = factory.Sequence(lambda n: n)


class CategoryFactory(django.DjangoModelFactory):
    FACTORY_FOR = Category

    name = factory.Sequence(lambda n: "Category %s" % n)
    group = factory.SubFactory(CategoryGroupFactory)
    order = factory.Sequence(lambda n: n)


class SubdomainFactory(django.DjangoModelFactory):
    FACTORY_FOR = Subdomain

    url = FuzzyText()
    title = FuzzyText()
    isCurrent = False
    status = Subdomain.ACTIVE
    order = fuzzy.FuzzyInteger(0)
    disclaimer = FuzzyText()
