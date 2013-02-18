# coding: utf-8

from django_webtest import WebTest

from message.models import Message


class TestSendMessage(WebTest):
    def setUp(self):
        self.form = self.app.get('/message/pomogite/dobavit').forms['mainForm']

    def tearDown(self):
        self.form = None

    def test_anonymous_message(self):
        before = Message.objects.count()
        self.form['title'] = 'Test message'
        self.form['message'] = "This is simple test message"
        self.form['contact_first_name'] = 'Dummy'
        self.form['contact_last_name'] = 'User'
        self.form['contact_mail'] = 'me@local.host'
        self.form['contact_phone'] = '123456789'
        self.form['address'] = 'Somewhere in the Earth'
        self.form.submit()
        self.assertEqual(before + 1, Message.objects.count())
