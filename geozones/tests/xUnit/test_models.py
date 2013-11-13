# -*- coding: utf-8 -*-

from django.test import TestCase

from geozones.factories import RegionFactory, LocationFactory


class TestRegion(TestCase):
    def setUp(self):
        self.region = RegionFactory.build()

    def tearDown(self):
        self.region = None

    def test_unicode(self):
        self.assertEqual(
            "%s" % self.region,
            self.region.name
        )


class TestLocation(TestCase):
    def setUp(self):
        self.location = LocationFactory.build()

    def tearDown(self):
        self.location = None

    def test_unicode(self):
        self.assertEqual(
            "%s" % self.location,
            "%f %f" % (self.location.latitude, self.location.longitude)
        )
