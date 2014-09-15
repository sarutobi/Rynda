# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django_webtest import WebTest
from post_office.models import Email

from test.factories import UserFactory


class TestUserRegistration(WebTest):
    """ Checks that the user can successfully register and activate account. """

    def setUp(self):
        self.site = Site.objects.get()
        self.site.domain = "example.com"
        self.site.name = "Example site"
        self.site.save()

    def action_registration(self):
        """ User fills registration form """
        page = self.app.get(reverse("user-creation"))
        form = page.forms["registration_form"]
        user = UserFactory.attributes(create=False)
        form["first_name"] = user['first_name']
        form["last_name"] = user['last_name']
        form["email"] = user['email']
        form["password1"] = "123"
        form["password2"] = "123"
        response = form.submit()
        return response

    def test_registration_page(self):
        users = User.objects.count()
        page = self.action_registration()
        self.assertEqual(200, page.status_code)
        self.assertTemplateUsed("registration_success.html")
        self.assertEqual(users+1, User.objects.count())

    def test_registration_email(self):
        """ Tests for account activation email """
        activation_string = "http://{}/user".format(self.site.domain)
        self.action_registration()
        mail = Email.objects.get()
        self.assertEqual("Account activation", mail.subject)
        self.assertIn(
            activation_string, mail.message, mail.message.encode('utf-8'))
        self.assertIn(activation_string, mail.html_message)
