# -*- coding: utf-8 -*-

from django.test import TestCase

from geozones.factories import LocationFactory, RegionFactory
from geozones.forms import LocationForm


class TestLocationForm(TestCase):
    """ Test forms for input locations """

    def setUp(self):
        region = RegionFactory()
        self.data = LocationFactory.attributes()
        self.data['region'] = region.pk

    def test_complete_form(self):
        form = LocationForm(data=self.data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid(), form.errors)

    def test_no_region(self):
        self.data['region'] = None
        form = LocationForm(data=self.data)
        self.assertTrue(form.is_valid(), form.errors)
