# -*- coding: utf-8 -*-

from django.test import TestCase

import floppyforms.__future__ as forms

from core.factories import FuzzyGeometryCollection
from message.factories import MessageFactory
from message.forms import (
    MessageForm, UserMessageForm, RequestForm, OfferForm, InformationForm)
from message.models import Message

from test.factories import UserFactory


class TestBaseMessageForm(TestCase):
    """Base message form tests"""
    def setUp(self):
        self.user = UserFactory()
        self.data = MessageFactory.attributes(
            create=False, extra={'user': self.user, }
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


class MessageDataGenerator(TestCase):
    def setUp(self):
        self.contacts = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'me@local.host',
            'phone': '1234567890',
        }
        loc_data = {
            'coordinates': FuzzyGeometryCollection().fuzz(),
            'address': 'test address',
        }
        self.data = MessageFactory.attributes(create=False)
        self.data.update(self.contacts)
        self.data.update(loc_data)


class TestUserMessageForm(MessageDataGenerator):

    def test_messagetype_widget(self):
        form = UserMessageForm()
        self.assertIsInstance(
            form.fields['messageType'].widget, forms.HiddenInput)

    def test_correct_form(self):
        """ Тест проверки правильной формы """
        form = UserMessageForm(data=self.data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid(), form.errors)

    def test_create_message(self):
        form = UserMessageForm(data=self.data)
        msg = form.save(commit=False)
        self.assertIsNotNone(msg)

    def test_store_message(self):
        form = UserMessageForm(data=self.data)
        msg = form.save(commit=False)
        msg.user = UserFactory()
        msg.save()
        self.assertEqual(1, Message.objects.count())

    def test_contact_data(self):
        """ Тестирование сохранения контактных данных """
        form = UserMessageForm(data=self.data)
        msg = form.save(commit=False)
        self.assertIsNotNone(msg.additional_info)
        self.assertEqual(msg.additional_info, self.contacts)

    def test_email_only(self):
        """ Введен только email """
        self.data['phone'] = ''
        form = UserMessageForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_message_status(self):
        form = UserMessageForm(data=self.data)
        msg = form.save(commit=False)
        self.assertEqual(msg.status, Message.NEW)

    def test_phone_only(self):
        """ Введен только телефон """
        self.data['email'] = ''
        form = UserMessageForm(data=self.data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_no_contact_data(self):
        """ Контактные данные не представлены """
        self.data['email'] = ''
        self.data['phone'] = ''
        form = UserMessageForm(data=self.data)
        self.assertFalse(form.is_valid())


class TestFormTypes(MessageDataGenerator):

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
