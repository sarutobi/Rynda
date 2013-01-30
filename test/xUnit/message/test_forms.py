# coding: utf-8

import unittest

from message.forms import SimpleRequestForm
from test.utils import lorem_ipsum, generate_string
from test.factories import UserFactory


class TestSimpleRequestForm(unittest.TestCase):

    def setUp(self):
        self.form = SimpleRequestForm()
        self.user = UserFactory.build()

    def tearDown(self):
        self.form = None
        self.user = None

    def test_form_type(self):
        self.assertEqual(1, self.form.fields['messageType'].initial)

    def test_send_data(self):
        data = {
            'message': lorem_ipsum(),
            'contact_first_name': self.user.first_name,
            'contact_last_name': self.user.last_name,
            'contact_mail': self.user.email
        }
        form = SimpleRequestForm(data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
