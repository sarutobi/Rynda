# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django_webtest import WebTest
from post_office.models import Email, EmailTemplate

from rynda.test.factories import UserFactory
from rynda.users.models import UserAuthCode


class TestUserRegistration(WebTest):
    """ Checks that the user can successfully register and activate account. """

    def setUp(self):
        self.site = Site.objects.get()
        self.site.domain = "example.com"
        self.site.name = "Example site"
        self.site.save()
        confirm = EmailTemplate(
            name='registration confirmation',
            subject='Account activation',
            content='http://{{site.domain}}/user/activate/{{user.id}}/{{activation_code}}',
            html_content='http://{{site.domain}}/user/activate/{{user.id}}/{{activation_code}}',
        )
        confirm.save()
        complete = EmailTemplate(
            name='registration complete',
            subject='Welcome to team !',
        )
        complete.save()

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
        """ User create account """
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

    def test_activation_link(self):
        """ Click on auto-activation link """
        self.action_registration()
        user = User.objects.all().order_by('-id')[0]
        self.assertFalse(user.is_active)
        activation_code = UserAuthCode(settings.SECRET_KEY).auth_code(user)
        activation_url = "/user/activate/{0}/{1}/".format(user.id, activation_code)
        page = self.app.get(activation_url).follow()
        self.assertEqual(200, page.status_code)
        self.assertTrue(User.objects.get(id=user.id).is_active)
        self.assertTemplateUsed("login.html")
        email = Email.objects.all().order_by("-id")[0]
        self.assertEqual(user.email, email.to[0])
        self.assertEqual(u"Welcome to team !", email.subject)

    def test_logged_in(self):
        """ Logged in user attempts to get registration form """
        user = UserFactory.create(is_active=True)
        page = self.app.get(reverse("user-creation"), user=user)
        self.assertRedirects(
            page, reverse("user-details", kwargs={'pk': user.id, }))
