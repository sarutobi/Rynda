# coding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse

from django_webtest import WebTest

from rynda.core.factories import FuzzyGeometryCollection, FuzzyPoint
from rynda.geozones.models import Location
from rynda.message.models import Message
from rynda.message.factories import MessageFactory
from rynda.test.factories import UserFactory


class MessageDataMixin():
    """  Provide additional message data, fill and send form """

    def generate_message(self):
        """ Populate factory-generated data with custom fields """
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
        self.data = MessageFactory.attributes(create=False)
        self.data.update(contacts)
        self.data.update(loc_data)

    def fill_form(self):
        """ Fill form and send it """
        form = self.page.forms['mainForm']
        form['title'] = self.data['title']
        form['message'] = self.data['message']
        form['is_anonymous'] = self.data['is_anonymous']
        form['allow_feedback'] = self.data['allow_feedback']
        form['email'] = self.data['email']
        form['address'] = self.data['address']
        form['coordinates'] = self.data['coordinates']
        form.submit()


class TestAnonymousMessage(WebTest, MessageDataMixin):
    """ Anonymous message """

    def setUp(self):
        self.page = self.app.get(reverse('message-create-request'))
        self.generate_message()

    def test_store_anonymous_message(self):
        """ Anonymous message has been stored """
        before = Message.objects.count()
        self.fill_form()
        self.assertEquals(before + 1, Message.objects.count())

    def test_message_is_anonymous(self):
        """ This message has been sent by anonymous """
        self.fill_form()
        msg = Message.objects.get()
        self.assertEqual(msg.user_id, settings.ANONYMOUS_USER_ID)


class TestSendRequestMessage(WebTest, MessageDataMixin):
    """ Request form """

    def setUp(self):
        self.user = UserFactory()
        self.page = self.app.get(
            reverse('message-create-request'),
            user=self.user.username)
        self.generate_message()

    def test_message_saved(self):
        before = Message.objects.count()
        self.fill_form()
        self.assertEquals(before + 1, Message.objects.count())

    def test_message_type(self):
        self.fill_form()
        msg = Message.objects.get()
        self.assertEqual(Message.REQUEST, msg.messageType)


class TestRequestMessageParameters(WebTest, MessageDataMixin):
    """ Tests for new request parameters """
    def setUp(self):
        self.user = UserFactory()
        self.page = self.app.get(
            reverse('message-create-request'),
            user=self.user.username
        )
        self.generate_message()

    def test_message_user(self):
        """ Test message author """
        self.fill_form()
        msg = Message.objects.get()
        self.assertEquals(msg.user, self.user)

    def test_message_flags(self):
        """ Test default message flags """
        self.fill_form()
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
        self.fill_form()
        msg = Message.objects.get()
        self.assertFalse(msg.is_anonymous)

    def test_no_feedback(self):
        """ Send message and do not want feedback """
        self.data['allow_feedback'] = False
        self.fill_form()
        msg = Message.objects.get()
        self.assertFalse(msg.allow_feedback)

    def test_message_location(self):
        loc_cnt = Location.objects.count()
        self.fill_form()
        self.assertEqual(loc_cnt + 1, Location.objects.count())
