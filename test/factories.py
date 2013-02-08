# coding: utf-8

import string
import factory
import random

from django.contrib.auth.models import User

from message.models import Message, MessageType
from test.utils import generate_string, lorem_ipsum


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    first_name = "Boy"
    last_name = "Factory"
    email = factory.LazyAttribute(
        lambda a:
        "{0}_{1}@example.com".format(a.first_name, a.last_name).lower())
    username = factory.Sequence(lambda n: "username_%s" % n)


class MessageFactory(factory.Factory):
    '''
    Factory for messages
    '''
    FACTORY_FOR = Message

    message = lorem_ipsum()
    contact_first_name = factory.Sequence(lambda n: "user_%s" % n)
    contact_last_name = factory.Sequence(lambda n: "name_%s" % n)
    contact_mail = factory.LazyAttribute(
        lambda a:
        "{0}_{1}@example.com".format(
            a.contact_first_name,
            a.contact_last_name
        ).lower())
    contact_phone = generate_string(str_len=10, src=string.digits)
    user = factory.SubFactory(UserFactory)
    messageType = random.randint(
        MessageType.TYPE_REQUEST, MessageType.TYPE_INFO)
