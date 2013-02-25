# coding: utf-8

import unittest

from django.core.exceptions import ValidationError

from geozones.factories import RegionFactory
from message.factories import MessageFactory
from test.factories import UserFactory


class TestMessage(unittest.TestCase):
    '''
    Test messages
    '''
    def setUp(self):
        self.user = UserFactory()
        self.region = RegionFactory()
        self.message = MessageFactory.build(georegion=self.region)

    def tearDown(self):
        self.user.delete()
        self.region.delete()
        self.message = None

    def test_message_unicode(self):
        self.assertEqual(self.message.title, "%s" % self.message)

    def test_message_save(self):
        self.message.save()
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


class TestMessageCleanData(unittest.TestCase):
    '''
    Test message cleaf functionality.
    '''
    def setUp(self):
        self.user = UserFactory()
        self.region = RegionFactory()
        self.message = MessageFactory.build(georegion=self.region)

    def tearDown(self):
        self.message = None
        self.region.delete()
        self.user.delete()

    def catch_wrong_data(self):
        ''' Common test missed data'''
        with self.assertRaises(ValidationError):
            self.message.save()
            self.message.delete()

    def test_no_message_contacts(self):
        self.message.contact_phone = None
        self.message.contact_mail = None
        self.catch_wrong_data()

    def test_invalid_email(self):
        self.message.contact_mail = 'notamail'
        self.catch_wrong_data()

    def test_phone_contact(self):
        self.message.contact_mail = ''
        self.message.save()
        self.assertIsNotNone(self.message.pk)
        self.message.delete()

    def test_email_contact(self):
        self.message.contact_phone = ''
        self.message.save()
        self.assertIsNotNone(self.message.pk)
        self.message.delete()


class TestUserMessage(unittest.TestCase):
    def setUp(self):
        self.user = UserFactory()

    def tearDown(self):
        self.user.delete()
        self.user = None

    def test_user_message(self):
        msg = MessageFactory(user=self.user)
        self.assertIsNotNone(msg)
        self.assertEqual(self.user, msg.user)


class TestMessageLocation(unittest.TestCase):
    def setUp(self):
        self.message = MessageFactory()

    def tearDown(self):
        user = self.message.user
        self.message.delete()
        user.delete()

    def test_location_latitude(self):
        self.assertIsNotNone(self.message.location.x)

    def test_location_longitude(self):
        self.assertIsNotNone(self.message.location.y)

    def test_location(self):
        self.assertIsNotNone(self.message.location)
