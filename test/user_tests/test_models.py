# coding: utf-8

import unittest
from test.factories import UserFactory

from django.contrib.auth.models import User
from django.db.models.signals import post_save

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

