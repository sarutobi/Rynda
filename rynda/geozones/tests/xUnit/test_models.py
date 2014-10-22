# -*- coding: utf-8 -*-

from django.contrib.gis.geos import Point, GeometryCollection
from django.test import TestCase

from rynda.geozones.factories import RegionFactory, LocationFactory


class TestRegion(TestCase):
    def setUp(self):
        self.region = RegionFactory.build()

    def test_unicode(self):
        self.assertEqual(
            "%s" % self.region,
            self.region.name
        )


class TestLocation(TestCase):
    """ Tests for location model """
    def setUp(self):
        self.region = RegionFactory()
        self.location = LocationFactory(region=self.region)

    def test_unicode(self):
        self.assertEqual(
            "%s" % self.location, self.location.name)

    def test_point_conversion(self):
        p = Point(0, 0)
        gc = GeometryCollection(p).wkt
        self.location.to_geocollection(p)
        self.assertEquals(self.location.coordinates.wkt, gc)
