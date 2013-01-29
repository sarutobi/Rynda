# coding: utf-8

import unittest
from test.factories import UserFactory

from django.contrib.auth.models import User
from django.db.models.signals import post_save

from core.backends import IonAuth
from users.models import create_new_user, Users


class UserTest(unittest.TestCase):
    '''User-specific tests'''
    def setUp(self):
        self.user = UserFactory.build()

    def tearDown(self):
        self.user = None

    def test_user(self):
        self.assertNotEqual(None, self.user)
        self.assertEqual('Boy', self.user.first_name)
        self.assertEqual('Factory', self.user.last_name)
        self.assertEqual('boy_factory@example.com', self.user.email)

    def test_user_generator(self):
        pass

    def test_create_new_user(self):
        self.assertEqual(0, User.objects.all().count())
        create_new_user(
            first_name = self.user.first_name,
            last_name = self.user.last_name,
            email = self.user.email,
            password='123'
        )
        self.assertEqual(1, User.objects.all().count())
        u = User.objects.get(email=self.user.email)
        self.assertEqual(u.first_name, self.user.first_name)
        self.assertEqual(u.last_name, self.user.last_name)
        self.assertTrue(u.check_password('123'))
        self.assertFalse(u.is_staff)
        self.assertFalse(u.is_active)


class AuthTest(unittest.TestCase):
    '''Authorization tests'''
    def test_ion_auth(self):
        self.assertEquals(40, len(self.user.password))
        
    def setUp(self):
        self.user = UserFactory.build(
            password = IonAuth().password_hash('123')
        )

    def tearDown(self):
        self.user = None

    def test_password_rewrite(self):
        self.user.save()
        ion_pass = self.user.password
        ion = IonAuth()
        u2 = ion.authenticate(self.user.email, '123')
        self.assertIsNotNone(u2)
        self.assertFalse(u2.is_anonymous())
        self.assertNotEqual(self.user.password, u2.password)
        self.user.delete()

