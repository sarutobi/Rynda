# -*- coding: utf-8 -*-

from django.test import TestCase
from django.utils.translation import ugettext as _

from rynda.users.forms import SimpleRegistrationForm
from rynda.users.models import Profile
from rynda.test.factories import UserFactory


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
        user = UserFactory()
        self.data['email'] = user.email
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
