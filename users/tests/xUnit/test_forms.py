# -*- coding: utf-8 -*-

from django.test import TestCase
from django.utils.translation import ugettext as _

from users.forms import (SimpleRegistrationForm, ForgotPasswordForm)
from users.models import Profile
from test.factories import UserFactory


class SimpleRegistrationFormTest(TestCase):
    ''' Registration form test'''

    def setUp(self):
        self.data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test_user@mail.ru',
            'password1': '123',
            'password2': '123'
        }
        self.user = UserFactory()

    def tearDown(self):
        self.data = None
        self.user.delete()
        Profile.objects.all().delete()

    def test_user_creation(self):
        form = SimpleRegistrationForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_lost_firstname(self):
        self.data['first_name'] = None
        form = SimpleRegistrationForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual([_(u'This field is required.'), ],
                         form['first_name'].errors)

    def test_empty_firstname(self):
        self.data['first_name'] = '   '
        form = SimpleRegistrationForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual([_(u'You must provide a first name!'), ],
                         form['first_name'].errors)

    def test_lost_lastname(self):
        self.data['last_name'] = None
        form = SimpleRegistrationForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual([_(u'This field is required.'), ],
                         form['last_name'].errors)

    def test_empty_lastname(self):
        self.data['last_name'] = '   '
        form = SimpleRegistrationForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual([_(u'You must provide a last name!'), ],
                         form['last_name'].errors)

    def test_existing_email(self):
        self.data['email'] = self.user.email
        form = SimpleRegistrationForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual([_(u'This email already registered'), ],
                         form['email'].errors)

    def test_passwords_diff(self):
        self.data['password1'] = 'qwe'
        form = SimpleRegistrationForm(self.data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual([_(u'The password fields did not match'), ],
                         form.errors['__all__'])


class TestForgotPasswordForm(TestCase):
    '''
    First step reset password functionality - validate email 
    '''

    def setUp(self):
        self.user = UserFactory()

    def tearDown(self):
        self.user.delete()

    def test_reset_password(self):
        data = {'email': self.user.email}
        form = ForgotPasswordForm(data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_unknown_email(self):
        data = {'email': 'mail@unexist.host',}
        form = ForgotPasswordForm(data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual([_(u'This email isn\'t registered'),],
            form['email'].errors)
