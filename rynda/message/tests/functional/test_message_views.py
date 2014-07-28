# coding: utf-8

from django_webtest import WebTest

from django.core.urlresolvers import reverse
from message.factories import MessageFactory
from message.models import Message

from test.factories import UserFactory


class TestMessagesList(WebTest):

    def setUp(self):
        self.page = self.app.get('/message/')

    def tearDown(self):
        self.page = None

    def test_list_code(self):
        self.assertEqual(200, self.page.status_code)

    def test_list_title(self):
        self.page.mustcontain("Список сообщений")


class TestMessagePaginator(WebTest):
    def setUp(self):
        self.user = UserFactory()
        for x in xrange(50):
            MessageFactory(status=2, user=self.user)
        self.page = self.app.get('/message/')

    def tearDown(self):
        Message.objects.all().delete()
        self.page = None

    def test_paginator_title(self):
        self.page.mustcontain("Сообщений на странице", "Назад", "Вперед")

    def test_page_count(self):
        self.page.mustcontain('1', '2', '3', '4', '5')


class TestMessageCreation(WebTest):
    """ Test message creation """
    def setUp(self):
        self.user = UserFactory()

    def test_creation_form(self):
        form = self.app.get(reverse("create-request")).form
        self.assertEquals("", form.action)
        self.assertEquals(form.method.upper(), 'POST')
