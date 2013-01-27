# coding: utf-8

import unittest
from test.factories import UserFactory

from django.contrib.auth.models import User
from django.db.models.signals import post_save

from users.models import create_user_profile, Users


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


class UserProfileTest(unittest.TestCase):
    '''User profile test'''
    def test_post_save_signal(self):
        # Disconnect post_save signal from user model (for test purposing only)
        post_save.disconnect(create_user_profile, sender=User)
        sender = User
        user = UserFactory.create()
        create_user_profile(sender, user, True)
        cnt = Users.objects.all().count()
        self.assertEqual(1, cnt)
