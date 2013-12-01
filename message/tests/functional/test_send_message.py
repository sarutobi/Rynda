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
        self.assertEquals(before +1, Message.objects.count())
#    def test_anonymous_form(self):
#        form = self.app.get('/message/pomogite/dobavit').forms['mainForm']
#        self.assertIsNone(form['user'])

#    def test_anonymous_message(self):
#        before = Message.objects.count()
#        self.form['title'] = 'Test message'
#        self.form['message'] = "This is simple test message"
#        self.form['georegion'] = self.region.pk
#        self.form['address'] = 'Some address string'
#        self.form.submit()
#        self.assertEqual(before + 1, Message.objects.count())

    # def test_knownuser_form(self):
        # ''' Form for authenticated user contain initial data for some fields'''
        # user = UserFactory(is_active=True)
        # form = self.app.get(
            # '/message/pomogite/dobavit',
            # user=user.username).forms['mainForm']
        # self.assertIsNotNone(form)
        # user.delete()

#    def test_knownuser_message(self):
#        ''' Authenticated user send message and this message must be
#            linked to user profile'''
#        before = Message.objects.count()
#        user = UserFactory(is_active=True)
#        form = self.app.get(
#            '/message/pomogite/dobavit',
#            user=user.username).forms['mainForm']
#        form['title'] = 'Test message'
#        form['message'] = "This is simple test message"
#        form['georegion'] = self.region.pk
#        form['address'] = 'Some address'
#        form.submit()
#        self.assertEqual(before + 1, Message.objects.count())
#        msg = Message.objects.all().select_related().reverse()[0]
#        self.assertEqual(msg.user, user)
#        user.delete()
