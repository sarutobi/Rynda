# coding: utf-8

import string
import factory

from django.contrib.auth.models import User

from message.models import Message
from test.utils import generate_string, lorem_ipsum


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    first_name = "Boy"
    last_name = "Factory"
    email = factory.LazyAttribute(
        lambda a:
        "{0}_{1}@example.com".format(a.first_name, a.last_name).lower())


class MessageFactory(factory.Factory):
    '''
    Factory for messages
    '''
    FACTORY_FOR = Message

    message = lorem_ipsum()
    contact_first_name = generate_string()
    contact_last_name = generate_string()
    contact_mail = factory.LazyAttribute(
        lambda a:
        "{0}_{1}@example.com".format(
            a.contact_first_name,
            a.contact_last_name
        ).lower())
    contact_phone = generate_string(str_len=10, src=string.digits)
