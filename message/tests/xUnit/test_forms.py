# coding: utf-8

import unittest

from core.factories import CategoryFactory

from geozones.factories import RegionFactory

from message.models import MessageType, Category

from message.forms import SimpleRequestForm
from test.utils import lorem_ipsum
from test.factories import UserFactory


class TestSimpleRequestForm(unittest.TestCase):

    def setUp(self):
        self.form = SimpleRequestForm()
        self.user = UserFactory()
        self.region = RegionFactory()
        self.data = {
            'title': lorem_ipsum(words_count=3),
            'message': lorem_ipsum(),
            'messageType': MessageType.TYPE_REQUEST,
            'georegion': self.region.pk,
            'location_0': 0.0,
            'location_1': 0.0,
            'address': lorem_ipsum(words_count=4)
        }

    def tearDown(self):
        self.region.delete()
        self.region = None
        self.form = None
        self.user.delete()

    def test_form_type(self):
        self.assertEqual(
            MessageType.TYPE_REQUEST,
            self.form.fields['messageType'].initial)

    def test_send_data(self):
        form = SimpleRequestForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid(), form.errors)
        msg = form.save(commit=False)
        msg.user = self.user
        msg.save()
        self.assertIsNotNone(msg)
        self.assertIsNotNone(msg.pk)
        self.assertEqual(1, msg.status)
        self.assertEqual(1, msg.messageType)
        msg.delete()


class TestRequestCategory(unittest.TestCase):
    def setUp(self):
        self.cats = list()
        for x in xrange(5):
            self.cats.append(CategoryFactory())
        self.user = UserFactory()
        self.region = RegionFactory()
        self.data = {
            'message': lorem_ipsum(),
            'messageType': MessageType.TYPE_REQUEST,
            'user_id': self.user,
            'georegion': self.region.pk,
            'location_0': 25.0,
            'location_1': 50.0,
            'category': [x.pk for x in self.cats],
            'address': lorem_ipsum(words_count=4)
        }

    def tearDown(self):
        Category.objects.all().delete()

    def test_message_with_cats(self):
        form = SimpleRequestForm(self.data)
        self.assertTrue(form.is_valid())
        msg = form.save(commit=False)
        msg.user = self.user
        msg.save()
        form.save_m2m()
        self.assertEqual(5, msg.category.all().count())


class TestRequiredFields(unittest.TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.region = RegionFactory()
        self.data = {
            'message': lorem_ipsum(),
            'messageType': MessageType.TYPE_REQUEST,
            'user': self.user,
            'address': lorem_ipsum(words_count=4),
            'georegion': self.region.pk,
            'location_0': 25.0,
            'location_1': 50.0,
        }

    def tearDown(self):
        self.region.delete()
        self.user = None
        self.data = None

    #def test_lost_address(self):
    #    self.data['address'] = ''
    #    form = SimpleRequestForm(self.data)
    #    self.assertFalse(form.is_valid())

    def test_lost_message(self):
        self.data['message'] = ''
        form = SimpleRequestForm(self.data)
        self.assertFalse(form.is_valid())

#    def test_lost_first_name(self):
#        self.data['contact_first_name'] = ''
#        form = SimpleRequestForm(self.data)
#        self.assertFalse(form.is_valid())

#    def test_lost_last_name(self):
#        self.data['contact_last_name'] = ''
#        form = SimpleRequestForm(self.data)
#        self.assertFalse(form.is_valid())

#    def test_lost_contacts(self):
#        self.data['contact_mail'] = ''
#        self.data['contact_phone'] = ''
#        form = SimpleRequestForm(self.data)
#        self.assertFalse(form.is_valid())

#    def test_lost_email(self):
#        self.data['contact_mail'] = ''
#        form = SimpleRequestForm(self.data)
#        self.assertTrue(form.is_valid(), form.errors)

#    def test_lost_phone(self):
#        self.data['contact_phone'] = ''
#        form = SimpleRequestForm(self.data)
#        self.assertTrue(form.is_valid())
