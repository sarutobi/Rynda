# coding: utf-8

from django_webtest import WebTest

from django.core.urlresolvers import reverse
from rynda.message.factories import MessageFactory
from rynda.message.models import Message

from rynda.test.factories import UserFactory


class TestMessagesList(WebTest):
    def setUp(self):
        self.page = self.app.get(reverse('messages-list'))

    def tearDown(self):
        self.page = None

    def test_list_code(self):
        self.assertEqual(200, self.page.status_code)

    def test_list_title(self):
        self.page.mustcontain("Message list")


class TestMessagePaginator(WebTest):
    def setUp(self):
        self.user = UserFactory()
        for x in xrange(50):
            MessageFactory(status=2, user=self.user)
        self.page = self.app.get(reverse('messages-list'))

    def tearDown(self):
        Message.objects.all().delete()
        self.page = None

    def test_paginator_title(self):
        self.page.mustcontain(u"Messages on page", u"Previous", u"Next")

    def test_page_count(self):
        self.page.mustcontain('1', '2', '3', '4', '5')


class TestMessageCreation(WebTest):
    """ Test message creation """
    def setUp(self):
        self.user = UserFactory()

    def test_creation_form(self):
        form = self.app.get(reverse("message-create-request")).form
        self.assertEquals("", form.action)
        self.assertEquals(form.method.upper(), 'POST')
