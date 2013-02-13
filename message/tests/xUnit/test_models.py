# coding: utf-8

import unittest

from django.core.exceptions import ValidationError

from message.factories import MessageFactory
from test.factories import UserFactory


class TestMessage(unittest.TestCase):
    '''
    Test messages
    '''
    def setUp(self):
        self.user = UserFactory()
        self.message = MessageFactory.build()
        self.message.user = self.user.pk

    def tearDown(self):
        self.user.delete()
        self.message = None

    def test_message(self):
        self.message.save()
        self.assertIsNotNone(self.message.pk)

    def catch_wrong_data(self):
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

    def test_message_remove(self):
        self.message.remove()
        self.assertTrue(self.message.is_removed())

    def test_message_restore(self):
        self.message.remove()
        self.assertTrue(self.message.is_removed())
        self.message.restore()
        self.assertFalse(self.message.is_removed())


class TestUserMessage(unittest.TestCase):
    def setUp(self):
        self.user = UserFactory()

    def tearDown(self):
        self.user.delete()
        self.user = None

    def test_user_message(self):
        msg = MessageFactory(user=self.user.pk)
        self.assertIsNotNone(msg)
        self.assertEqual(self.user.pk, msg.user)
