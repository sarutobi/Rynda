# -*- coding: utf-8 -*-


import floppyforms as forms
from django.test import TestCase

from core.factories import CategoryFactory, SubdomainFactory
from geozones.factories import RegionFactory
from message.factories import MessageFactory
from message.forms import (
    MessageForm, UserMessageForm, RequestForm, OfferForm, InformationForm)
from message.models import Message, Category

from test.factories import UserFactory


class TestBaseMessageForm(TestCase):
    """Base message form tests"""
    def setUp(self):
        self.user = UserFactory()
        subdomain = SubdomainFactory()
        self.data = MessageFactory.attributes(
            create=False, extra={
                'user': self.user, 'subdomain': subdomain.pk, }
        )

    def test_send_data(self):
        form = MessageForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid(), form.errors)
        msg = form.save(commit=False)
        self.assertIsNotNone(msg)
        self.assertEqual(Message.NEW, msg.status)
        self.assertEqual(self.data['messageType'], msg.messageType)

    def test_lost_message(self):
        self.data["message"] = ""
        form = MessageForm(self.data)
        self.assertFalse(form.is_valid())

    # def test_virtual_message(self):
        # virtual_message = MessageFactory.attributes(
            # create=False, extra={'user': self.user, 'is_virtual': True}
        # )
        # form = MessageForm(data=virtual_message)
        # self.assertTrue(form.is_valid())
        # msg = form.save(commit=False)
        # self.assertIsNone(msg.linked_location)

    # def test_ordinal_message(self):
        # form = MessageForm(data=self.data)
        # msg = form.save(commit=False)
        # self.assertEquals(self.data['linked_location'], msg.linked_location)


class TestUserMessageForm(TestCase):
    def setUp(self):
        self.form = UserMessageForm()

    def test_messagetype_widget(self):
        self.assertIsInstance(
            self.form.fields['messageType'].widget,
            forms.HiddenInput)


class TestFormTypes(TestCase):

    def setUp(self):
        self.region = RegionFactory()
        subdomain = SubdomainFactory()
        self.data = MessageFactory.attributes(
            create=False, extra={
                'messageType': Message.REQUEST, 'subdomain': subdomain.pk,
            }
        )

    def test_request_form(self):
        form = RequestForm()
        self.assertEqual(Message.REQUEST, form.fields['messageType'].initial)
        self.data['messageType'] = Message.OFFER
        form = RequestForm(self.data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(Message.REQUEST, form.cleaned_data['messageType'])

    def test_offer_form(self):
        form = OfferForm()
        self.assertEqual(Message.OFFER, form.fields['messageType'].initial)
        form = OfferForm(self.data)
        self.assertTrue(form.is_valid())
        self.assertEqual(Message.OFFER, form.cleaned_data['messageType'])

    def test_info_form(self):
        form = InformationForm()
        self.assertEqual(Message.INFO, form.fields['messageType'].initial)
        form = InformationForm(self.data)
        self.assertTrue(form.is_valid())
        self.assertEqual(Message.INFO, form.cleaned_data['messageType'])


class TestRequestCategory(TestCase):
    def setUp(self):
        self.cats = list()
        for x in xrange(5):
            self.cats.append(CategoryFactory())
        # self.user = UserFactory()
        # self.region = RegionFactory()
# #        self.type_request = MessageTypeFactory()
        self.data = {
            # 'message': lorem_ipsum(),
            # 'user_id': self.user,
            # 'location_0': 25.0,
            # 'location_1': 50.0,
            'category': [x.pk for x in self.cats],
            # 'address': lorem_ipsum(words_count=4)
        }

    def tearDown(self):
        Category.objects.all().delete()

#    def test_message_with_cats(self):
#        form = UserMessageForm(self.data, message_type=self.type_request.pk)
#        self.assertTrue(form.is_valid())
#        msg = form.save(commit=False)
#        msg.user = self.user
#        msg.save()
#        form.save_m2m()
#        self.assertEqual(5, msg.category.all().count())


class TestRequiredFields(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.region = RegionFactory()
        self.data = {
            'message': lorem_ipsum(),
            'messageType': self.type_request.pk,
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

#    def test_lost_message(self):
#        self.data['message'] = ''
#        form = UserMessageForm(self.data, message_type=self.type_request.pk)
#        self.assertFalse(form.is_valid())

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
