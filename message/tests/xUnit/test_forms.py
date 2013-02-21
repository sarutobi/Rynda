# coding: utf-8

import unittest

from geozones.factories import RegionFactory

from message.models import MessageType
from message.forms import SimpleRequestForm
from test.utils import lorem_ipsum
from test.factories import UserFactory


class TestSimpleRequestForm(unittest.TestCase):

    def setUp(self):
        self.form = SimpleRequestForm()
        self.user = UserFactory.build()
        self.region = RegionFactory()
        self.data = {
            'title': lorem_ipsum(words_count=3),
            'message': lorem_ipsum(),
            'messageType': MessageType.TYPE_REQUEST,
            'contact_first_name': self.user.first_name,
            'contact_last_name': self.user.last_name,
            'contact_mail': self.user.email,
            'georegion': self.region.pk,
            'location_0': 0.0,
            'location_1': 0.0,
        }

    def tearDown(self):
        self.region = None
        self.form = None
        self.user = None

    def test_form_type(self):
        self.assertEqual(1, self.form.fields['messageType'].initial)

    def test_send_data(self):
        form = SimpleRequestForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid(), form.errors)
        msg = form.save(commit=True)
        self.assertIsNotNone(msg)
        self.assertIsNotNone(msg.pk)
        self.assertEqual(1, msg.status)
        self.assertEqual(0, msg.flags)
        self.assertEqual(1, msg.messageType)
        msg.delete()


class TestRequiredFields(unittest.TestCase):

    def setUp(self):
        self.user = UserFactory.build()
        self.region = RegionFactory.build()
        self.data = {
            'message': lorem_ipsum(),
            'messageType': MessageType.TYPE_REQUEST,
            'contact_first_name': self.user.first_name,
            'contact_last_name': self.user.last_name,
            'contact_mail': self.user.email,
            'address': lorem_ipsum(words_count=4),
        }

    def tearDown(self):
        self.user = None
        self.data = None

    def test_lost_address(self):
        self.data['address'] = ''
        form = SimpleRequestForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_lost_message(self):
        self.data['message'] = ''
        form = SimpleRequestForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_lost_first_name(self):
        self.data['contact_first_name'] = ''
        form = SimpleRequestForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_lost_last_name(self):
        self.data['contact_last_name'] = ''
        form = SimpleRequestForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

