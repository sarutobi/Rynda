# coding: utf-8

import factory
import random

from .models import City, Region


class CityFactory(factory.Factory):
    FACTORY_FOR = City

    name = factory.Sequence(lambda n: "City_%s" % n)
    latitude = random.uniform(-90.0, 90.0)
    longtitude = random.uniform(-180.0, 180.0)
    #region_id = factory.Sequence(lambda n: n)


class RegionFactory(factory.Factory):
    FACTORY_FOR = Region

    name = factory.Sequence(lambda n: "Region_%s" % n)
    cityId = factory.SubFactory(CityFactory)
    slug = factory.LazyAttribute(lambda a: a.name.lower())
    zoomLvl = random.randint(1, 10)
    order = factory.Sequence(lambda n: n)
