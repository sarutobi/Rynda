# coding: utf-8

import factory

from factory import django

from .models import Category, CategoryGroup


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
