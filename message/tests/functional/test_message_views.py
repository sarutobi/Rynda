# coding: utf-8

from django_webtest import WebTest

from message.factories import MessageFactory
from message.models import Message


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
        for x in xrange(50):
            MessageFactory(status=2)
        self.page = self.app.get('/message/')

    def tearDown(self):
        Message.objects.all().delete()
        self.page = None

    def test_paginator_title(self):
        self.page.mustcontain("Сообщений на странице", "Назад", "Вперед")

    def test_page_count(self):
        self.page.mustcontain('1', '2', '3', '4', '5')
