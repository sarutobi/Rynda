# coding: utf-8

import unittest

from test.factories import UserFactory

from core.backends import IonAuth, EmailAuthBackend


class AuthTest(unittest.TestCase):
    '''Authorization tests'''

    def setUp(self):
        self.user = UserFactory.build(
            password=IonAuth().password_hash('123'),
            is_active=True
        )

    def tearDown(self):
        self.user = None

    def test_ion_auth(self):
        self.assertEquals(40, len(self.user.password))

    def test_password_rewrite(self):
        '''
        If user enters correct ion password, backend will
        rehash password to django-specific password hash.
        '''
        self.user.save()
        ion = IonAuth()
        u2 = ion.authenticate(username=self.user.email, password='123')
        self.assertIsNotNone(u2)
        self.assertFalse(u2.is_anonymous())
        self.assertNotEqual(self.user.password, u2.password)
        self.user.delete()


class EmailBackendTest(unittest.TestCase):
    def setUp(self):
        self.user = UserFactory.build(
            email='test@example.com',
        )
        self.user.set_password('test')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_authenticate(self):
        auth = EmailAuthBackend()
        user = auth.authenticate(username='test@example.com', password='test')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)

