# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_webtest import WebTest

from test.factories import UserFactory


class TestUserRegistration(WebTest):
    """ Checks that the user can successfully register and activate account. """

    def setUp(self):
        site = Site.objects.get()
        site.domain = "example.com"
        site.save()

    def test_registration_page(self):
        page = self.app.get(reverse("user-creation"))
        self.assertEqual(200, page.status_code)
        page.mustcontain("Registration")
        # page.mustcontain("First name")
        # page.mustcontain("Last name")
        # page.mustcontain("Password")
        form = page.forms[0]
        user = UserFactory.attributes(create=False)
        form["first_name"] = user['first_name']
        form["last_name"] = user['last_name']
        form["email"] = user['email']
        form["password1"] = "123"
        form["password2"] = "123"
        response = form.submit()
        self.assertEqual(200, page.status_code)
        self.assertTemplateUsed("index.html")

