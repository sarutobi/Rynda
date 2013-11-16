# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
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
        self.assertEqual(self.message.title, "%s" % self.message)

    def test_message_flags(self):
        self.assertFalse(self.message.is_active)
        self.assertFalse(self.message.is_important)
        self.assertTrue(self.message.is_anonymous)
        self.assertFalse(self.message.is_removed)
        self.assertTrue(self.message.allow_feedback)

    def test_message_save(self):
        self.message.save()
        self.assertEqual(1, len(Message.objects.all()))
        self.assertIsNotNone(self.message.pk)
        self.message.delete()

    def test_message_remove(self):
        self.message.is_removed = True
        self.assertTrue(self.message.is_removed)

    def test_message_restore(self):
        self.message.is_removed = True
        self.assertTrue(self.message.is_removed)
        self.message.is_removed = False
        self.assertFalse(self.message.is_removed)


class TestMessageCleanData(TestCase):
    '''
    Test message cleaf functionality.
    '''
    def setUp(self):
        self.user = UserFactory()
        self.region = RegionFactory()
        self.message = MessageFactory.build(georegion=self.region)

#    def tearDown(self):
#        self.message = None
#        self.region.delete()
#        self.user.delete()

    def catch_wrong_data(self):
        ''' Common test missed data'''
        with self.assertRaises(ValidationError):
            self.message.save()
            self.message.delete()

#    def test_no_message_contacts(self):
#        self.message.contact_phone = None
#        self.message.contact_mail = None
#        self.catch_wrong_data()

#    def test_invalid_email(self):
#        self.message.contact_mail = 'notamail'
#        self.catch_wrong_data()

#    def test_phone_contact(self):
#        self.message.contact_mail = ''
#        self.message.save()
#        self.assertIsNotNone(self.message.pk)
#        self.message.delete()

#    def test_email_contact(self):
#        self.message.contact_phone = ''
#        self.message.save()
#        self.assertIsNotNone(self.message.pk)
#        self.message.delete()


class TestUserMessage(TestCase):
    def setUp(self):
        self.user = UserFactory()

#    def tearDown(self):
#        self.user.delete()
#        self.user = None

#    def test_user_message(self):
#        msg = MessageFactory(user=self.user)
#        self.assertIsNotNone(msg)
#        self.assertEqual(self.user, msg.user)


class TestMessageCategories(TestCase):
    def setUp(self):
        self.message = MessageFactory()
        self.category = CategoryFactory()

    def tearDown(self):
        self.message.delete()
        self.category.delete()

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
