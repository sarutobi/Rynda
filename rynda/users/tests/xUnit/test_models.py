# coding: utf-8

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase

from post_office.models import Email, EmailTemplate

from rynda.test.factories import UserFactory
from rynda.users.models import (
    UserAuthCode, create_new_user, activate_user, list_public_users)


class UserAuthCodeTest(TestCase):

    def setUp(self):
        self.encoder = UserAuthCode('secret')
        self.user = UserFactory(is_active=False)

    def test_user(self):
        self.assertIsNotNone(self.user.date_joined)
        self.assertTrue(self.user.date_joined >= self.user.last_login)

    def test_salt(self):
        salt = self.encoder.salt()
        self.assertEqual(8, len(salt))

    def test_auth_code(self):
        code = self.encoder.auth_code(self.user)
        self.assertIsNotNone(code)

    def test_complete_activation(self):
        code = self.encoder.auth_code(self.user)
        self.assertTrue(self.encoder.is_valid(self.user, code))

    def test_wrong_key(self):
        self.assertFalse(self.encoder.is_valid(self.user, 'aaa'))

    def test_already_activated(self):
        code = self.encoder.auth_code(self.user)
        self.user.last_login = timezone.now()
        self.user.save()
        self.assertFalse(self.encoder.is_valid(self.user, code))


class UserTest(TestCase):
    """ User-specific tests """
    def setUp(self):
        self.user = UserFactory.build(
            first_name='Boy',
            last_name='Factory'
        )

    def test_user(self):
        self.assertNotEqual(None, self.user)

    def test_user_first_name(self):
        self.assertEqual('Boy', self.user.first_name)

    def test_user_last_name(self):
        self.assertEqual('Factory', self.user.last_name)

    def test_user_email(self):
        self.assertEqual('boy_factory@mail.ru', self.user.email)


class TestUserCreation(TestCase):

    def setUp(self):
        user = UserFactory.build()
        confirm = EmailTemplate(
            name='registration confirmation',
            subject='Account activation',
        )
        confirm.save()
        self.before = User.objects.count()
        self.user = create_new_user(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password='123'
        )

    def test_create_new_user(self):
        self.assertEqual(self.before + 1, User.objects.all().count())

    def test_user_password(self):
        u = User.objects.get(email=self.user.email)
        self.assertTrue(u.check_password('123'))

    def test_user_staff(self):
        u = User.objects.get(email=self.user.email)
        self.assertFalse(u.is_staff)

    def test_user_active(self):
        u = User.objects.get(email=self.user.email)
        self.assertFalse(u.is_active)

    def test_send_email(self):
        emails_count = Email.objects.count()
        self.assertEqual(1, emails_count)

    def test_email_subject(self):
        mail = Email.objects.get()
        self.assertEqual(
            mail.subject,
            u'Account activation',
            mail.subject
        )

    def test_profile_creation(self):
        """ User mist have profile """
        self.assertIsNotNone(self.user.profile)


class TestUserActivation(TestCase):
    def setUp(self):
        encoder = UserAuthCode(settings.SECRET_KEY)
        self.user = UserFactory(is_active=False)
        self.code = encoder.auth_code(self.user)
        confirm = EmailTemplate(
            name='registration confirmation',
            subject='Account activation',
        )
        confirm.save()
        complete = EmailTemplate(
            name='registration complete',
        )
        complete.save()

    def test_user_activation(self):
        self.assertTrue(activate_user(self.user, self.code), self.user.email)
        self.assertTrue(self.user.is_active)

    def test_wrong_code(self):
        self.assertFalse(activate_user(self.user, 'self.code'))
        self.assertFalse(self.user.is_active)


class TestPublicUsers(TestCase):
    """ Tests for select only public users """
    def setUp(self):
        for x in xrange(10):
            u = UserFactory(is_active=True)
            u.profile.is_public = True
            u.profile.save()

    def test_active_public(self):
        """ Select only active and public """
        self.assertEquals(10, len(list_public_users()))

    def test_not_public(self):
        """ Do not show active users without public flag """
        u = UserFactory(is_active=True)
        u.profile.is_public = False
        u.profile.save()
        u.save()
        self.assertEquals(10, len(list_public_users()))

    def test_not_active(self):
        u = UserFactory(is_active=False)
        u.profile.is_public = True
        u.profile.save()
        self.assertEquals(10, len(list_public_users()))
