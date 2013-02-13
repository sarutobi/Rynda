# coding: utf-8

import factory
import random
import string

from test.utils import generate_string, lorem_ipsum
from test.factories import UserFactory

from .models import Message, MessageType


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
