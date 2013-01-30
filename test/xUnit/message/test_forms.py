# coding: utf-8

import unittest

from message.forms import SimpleRequestForm


class TestSimpleRequestForm(unittest.TestCase):

    def setUp(self):
        self.form = SimpleRequestForm()

    def tearDown(self):
        self.form = None

    def test_form_type(self):
        self.assertEqual(1, self.form.fields['messageType'].initial)
