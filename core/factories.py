# coding: utf-8

import factory
import random

from .models import City


class CityFactory(factory.Factory):
    FACTORY_FOR = City

    name = factory.Sequence(lambda n: "City_%s" % n)
    latitude = random.uniform(-90.0, 90.0)
    longtitude = random.uniform(-180.0, 180.0)
    #region_id = factory.Sequence(lambda n: n)
