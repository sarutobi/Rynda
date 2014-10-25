# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse_lazy

from rynda.message.factories import MessageFactory
from rynda.message.models import Message
from rynda.message.views import generate_message_pane, MAX_PANE_MESSAGES


class TestIndexPage(TestCase):
    """ Index page view tests """

    def setUp(self):
        for x in range(50):
            MessageFactory(status=Message.VERIFIED)

    def test_generate_offer_pane(self):
        query = Message.objects.active().type_is(Message.OFFER)[:MAX_PANE_MESSAGES+1]
        title = "Some title"
        link = reverse_lazy("messages-list")
        pane = generate_message_pane(title, query, link)
        self.assertIsNotNone(pane)

    def test_generate_request_pane(self):
        query = Message.objects.active().type_is(Message.REQUEST)[:MAX_PANE_MESSAGES+1]
        title = "Some title"
        pane = generate_message_pane(title, query)
        self.assertIsNotNone(pane)
