# coding: utf-8

from django.core.urlresolvers import reverse

from django_webtest import WebTest

from message.models import Message
from message.factories import MessageFactory
from test.factories import UserFactory


class TestSendRequestMessage(WebTest):
    """ Functional test for request creation. """

    def setUp(self):
        self.user = UserFactory()
        self.page = self.app.get(
            reverse('create-request'),
            user=self.user.username)
        self.data = MessageFactory.attributes(create=False)

    def tearDown(self):
        Message.objects.all().delete()

    def test_get_form(self):
        form = self.page.forms['mainForm']
        self.assertIsNotNone(form)

    def test_message_saved(self):
        before = Message.objects.count()
        form = self.page.forms['mainForm']
        form['title'] = self.data['title']
        form['message'] = self.data['message']
        form['is_anonymous'] = self.data['is_anonymous']
        form['allow_feedback'] = self.data['allow_feedback']
        form.submit()
        self.assertEquals(before + 1, Message.objects.count())


class TestRequestMessageParameters(WebTest):
    """ Test for new request parameters """
    def setUp(self):
        self.user = UserFactory()
        self.data = MessageFactory.attributes(create=False)
        form = self.app.get(
            reverse('create-request'), user=self.user.username
        ).forms['mainForm']
        form['title'] = self.data['title']
        form['message'] = self.data['message']
        form['is_anonymous'] = self.data['is_anonymous']
        form['allow_feedback'] = self.data['allow_feedback']
        form.submit()

    def test_message_user(self):
        """ Test message author """
        msg = Message.objects.get()
        self.assertEquals(msg.user, self.user)

    def test_message_flags(self):
        """ Test default message flags """
        msg = Message.objects.get()
        self.assertEquals(Message.NEW, msg.status)
        self.assertFalse(msg.is_removed)
        self.assertTrue(msg.is_anonymous)
        self.assertTrue(msg.allow_feedback)
        self.assertFalse(msg.is_virtual)
        self.assertFalse(msg.is_important)
        self.assertFalse(msg.is_active)
