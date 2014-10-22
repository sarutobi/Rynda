# -*- coding: utf-8 -*-

from django.test import TestCase

from rynda.core.factories import CategoryFactory


class TestCategory(TestCase):

    def test_category(self):
        cat = CategoryFactory()
        self.assertIsNotNone(cat)
        cat.delete()

    def test_category_unicode(self):
        cat = CategoryFactory()
        self.assertEqual(cat.name, "%s" % cat)
        cat.delete()
