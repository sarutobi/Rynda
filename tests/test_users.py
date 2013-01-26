# coding: utf-8

import unittest

from factories import UserFactory

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
