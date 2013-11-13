# -*- coding: utf-8 -*-

from django.test import TestCase

from core.factories import CategoryFactory, CategoryGroupFactory


class TestCategoryGroup(TestCase):

    def setUp(self):
        self.group = CategoryGroupFactory()

    def tearDown(self):
        self.group.delete()

    def test_group(self):
        self.assertIsNotNone(self.group)

    def test_group_unicode(self):
        expect = self.group.name
        self.assertEqual(expect, "%s" % self.group)

    def test_appeng_category(self):
        cat = CategoryFactory(group=None)
        self.group.add_category(cat)
        self.assertEqual(cat.group, self.group)
        cat.delete()


class TestCategory(TestCase):
    def setUp(self):
        self.group = CategoryGroupFactory()

    def tear_down(self):
        self.group.delete()

    def test_category(self):
        cat = CategoryFactory(group=self.group)
        self.assertIsNotNone(cat)
        self.assertEqual(cat.group, self.group)
        cat.delete()

    def test_unlinked_category(self):
        cat = CategoryFactory(group=None, subdomain=None)
        self.assertIsNotNone(cat)
        self.assertIsNone(cat.group)
        cat.delete()

    def test_category_unicoade(self):
        cat = CategoryFactory(group=self.group)
        self.assertEqual(cat.name, "%s" % cat)
        cat.delete()

    def test_unlink_category(self):
        cat = CategoryFactory(group=self.group)
        cat.unlink()
        self.assertIsNone(cat.group)
        cat.delete()
