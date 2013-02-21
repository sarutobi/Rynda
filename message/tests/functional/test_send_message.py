# coding: utf-8

from django_webtest import WebTest

from geozones.factories import RegionFactory
from message.models import Message
from test.factories import UserFactory


class TestSendMessage(WebTest):
    def setUp(self):
        self.region = RegionFactory()
        self.form = self.app.get('/message/pomogite/dobavit').forms['mainForm']

    def tearDown(self):
        Message.objects.all().delete()
        self.region.delete()
        self.form = None

    def test_anonymous_message(self):
        before = Message.objects.count()
        self.form['title'] = 'Test message'
        self.form['message'] = "This is simple test message"
        self.form['contact_first_name'] = 'Dummy'
        self.form['contact_last_name'] = 'User'
        self.form['contact_mail'] = 'me@local.host'
        self.form['contact_phone'] = '123456789'
        self.form['georegion'] = self.region.pk
        self.form.submit()
        self.assertEqual(before + 1, Message.objects.count())

    def test_knownuser_form(self):
        ''' Form for authenticated user contain initial data for some fields'''
        user = UserFactory(is_active=True)
        form = self.app.get(
            '/message/pomogite/dobavit',
            user=user.username).forms['mainForm']
        self.assertEqual(user.first_name, form['contact_first_name'].value)
        self.assertEqual(user.last_name, form['contact_last_name'].value)
        self.assertEqual(user.email, form['contact_mail'].value)
        self.assertEqual(user.profile.phones, form['contact_phone'].value)
        user.delete()

    def test_knownuser_message(self):
        ''' Authenticated user send message and this message must be
            linked to user profile'''
        before = Message.objects.count()
        user = UserFactory(is_active=True)
        form = self.app.get(
            '/message/pomogite/dobavit',
            user=user.username).forms['mainForm']
        form['title'] = 'Test message'
        form['message'] = "This is simple test message"
        form['georegion'] = self.region.pk
        form.submit().showbrowser()
        self.assertEqual(before + 1, Message.objects.count())
        msg = Message.objects.all().select_related().reverse()[0]
        self.assertEqual(msg.user, user)
        user.delete()
