# -*- coding: utf-8 -*-

from django.test import TestCase

from rynda.geozones.factories import RegionFactory


class TestRegion(TestCase):
    def setUp(self):
        self.region = RegionFactory.build()

    def test_unicode(self):
        self.assertEqual(
            "%s" % self.region,
            self.region.name
        )
