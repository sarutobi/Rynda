# coding: utf-8

import factory
import random
import string

from geozones.factories import RegionFactory
from test.utils import generate_string, lorem_ipsum
from test.factories import UserFactory

from .models import Message, MessageType


def point_gen(num):
    latitude = random.uniform(-90.0, 90.0)
    longitude = random.uniform(-180.0, 180.0)
    return "POINT(%f %f)" % (longitude, latitude)


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
    messageType = random.choice((
        MessageType.TYPE_REQUEST,
        MessageType.TYPE_RESPONSE,
        MessageType.TYPE_INFO))
    georegion = factory.SubFactory(RegionFactory)
    location = factory.LazyAttribute(lambda n: point_gen(n))
    address = factory.Sequence(lambda n: "address string %s" % n)
