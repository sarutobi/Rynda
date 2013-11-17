# -*- coding: utf-8 -*-

from django.test import TestCase

from core.factories import CategoryFactory
from geozones.factories import RegionFactory
from message.factories import MessageFactory
from message.models import Message
from test.factories import UserFactory


class TestMessage(TestCase):
    ''' Test core message functionality '''
    def setUp(self):
        self.user = UserFactory()
        self.region = RegionFactory()
        self.message = MessageFactory(
            user=self.user)

    def test_message_unicode(self):
        """ Test for message __unicode__ method"""
        self.assertEqual(self.message.title, "%s" % self.message)

    def test_message_flags(self):
        """ Testing message default flags """
        self.assertFalse(self.message.is_active)
        self.assertFalse(self.message.is_important)
        self.assertTrue(self.message.is_anonymous)
        self.assertFalse(self.message.is_removed)
        self.assertTrue(self.message.allow_feedback)

    def test_message_save(self):
        """ Test for double save messages """
        self.message.save()
        self.assertEqual(1, len(Message.objects.all()))
        self.assertIsNotNone(self.message.pk)
        self.message.delete()

    def test_message_status(self):
        """ Test for default message status """
        self.assertEquals(self.message.status, Message.NEW)


class TestMessageCategories(TestCase):
    def setUp(self):
        self.message = MessageFactory()
        self.category = CategoryFactory()

    def test_add_category(self):
        before = len(self.message.category.all())
        self.message.category.add(self.category)
        self.assertEqual(len(self.message.category.all()), before + 1)

    def test_added_category_stored(self):
        self.message.category.add(self.category)
        m = Message.objects.get(id=self.message.pk)
        self.assertIn(self.category, m.category.all())

    def test_added_category_twice(self):
        before = len(self.message.category.all())
        self.message.category.add(self.category)
        self.message.category.add(self.category)
        self.assertEqual(len(self.message.category.all()), before + 1)

    def test_remove_category(self):
        self.message.category.add(self.category)
        before = self.message.category.count()
        self.message.category.remove(self.category)
        self.assertNotIn(self.category, self.message.category.all())
        self.assertEqual(self.message.category.count(), before - 1)
