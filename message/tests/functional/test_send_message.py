# coding: utf-8

from django.core.urlresolvers import reverse

from django_webtest import WebTest

from core.factories import SubdomainFactory, FuzzyPoint
from message.models import Message
from message.factories import MessageFactory
from test.factories import UserFactory


class MessageDataMixin():
    def generate_message(self):
        contacts = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'me@local.host',
            'phone': '1234567890',
        }
        loc_data = {
            'coordinates': FuzzyPoint().fuzz(),
            'address': 'test address',
        }
        subdomain = SubdomainFactory()
        data = MessageFactory.attributes(
            create=False, extra={
                'subdomain': subdomain.pk, })
        data.update(contacts)
        data.update(loc_data)
        return data


class TestAnonymousMessage(WebTest, MessageDataMixin):
    """ Отправка сообщения незарегистрированным пользователем """

    def setUp(self):
        self.page = self.app.get(reverse('create-request'))
        self.data = self.generate_message()

    def test_anonymous_message(self):
        before = Message.objects.count()
        form = self.page.forms['mainForm']
        form['title'] = self.data['title']
        form['message'] = self.data['message']
        form['is_anonymous'] = self.data['is_anonymous']
        form['allow_feedback'] = self.data['allow_feedback']
        form['email'] = self.data['email']
        form['address'] = self.data['address']
        form['coordinates'] = self.data['coordinates']
        form.submit()
        self.assertEquals(before + 1, Message.objects.count())


class TestSendRequestMessage(WebTest, MessageDataMixin):
    """ Functional test for request creation. """

    def setUp(self):
        self.user = UserFactory()
        self.page = self.app.get(
            reverse('create-request'),
            user=self.user.username)
        self.data = self.generate_message()

    # def tearDown(self):
        # Message.objects.all().delete()

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
        form['email'] = self.data['email']
        form['address'] = self.data['address']
        form['coordinates'] = self.data['coordinates']
        form.submit()
        self.assertEquals(before + 1, Message.objects.count())


class TestRequestMessageParameters(WebTest, MessageDataMixin):
    """ Tests for new request parameters """
    def setUp(self):
        self.user = UserFactory()
        self.data = self.generate_message()
        self.form = self.app.get(
            reverse('create-request'), user=self.user.username
        ).forms['mainForm']

    def send_form(self):
        self.form['title'] = self.data['title']
        self.form['message'] = self.data['message']
        self.form['is_anonymous'] = self.data['is_anonymous']
        self.form['allow_feedback'] = self.data['allow_feedback']
        self.form['email'] = self.data['email']
        self.form['address'] = self.data['address']
        self.form['coordinates'] = self.data['coordinates']
        self.form.submit()

    def test_message_user(self):
        """ Test message author """
        self.send_form()
        msg = Message.objects.get()
        self.assertEquals(msg.user, self.user)

    def test_message_flags(self):
        """ Test default message flags """
        self.send_form()
        msg = Message.objects.get()
        self.assertEquals(Message.NEW, msg.status)
        self.assertFalse(msg.is_removed)
        self.assertTrue(msg.is_anonymous)
        self.assertTrue(msg.allow_feedback)
        self.assertFalse(msg.is_virtual)
        self.assertFalse(msg.is_important)
        self.assertFalse(msg.is_active)

    def test_nonanonymous_message(self):
        """ Send non-anonymous message """
        self.data['is_anonymous'] = False
        self.send_form()
        msg = Message.objects.get()
        self.assertFalse(msg.is_anonymous)

    def test_no_feedback(self):
        """ Send message and do not want feedback """
        self.data['allow_feedback'] = False
        self.send_form()
        msg = Message.objects.get()
        self.assertFalse(msg.allow_feedback)
