# coding: utf-8

import factory
import random

from geozones.factories import RegionFactory
from test.utils import lorem_ipsum
from test.factories import UserFactory

from .models import Message, MessageType


def point_gen(num):
    latitude = random.uniform(-90.0, 90.0)
    longitude = random.uniform(-180.0, 180.0)
    return "POINT(%f %f)" % (longitude, latitude)


class MessageTypeFactory(factory.Factory):
    """Factory for message types"""
    FACTORY_FOR = MessageType

    name = factory.Sequence(lambda n: "message type %s" % n)


class MessageFactory(factory.Factory):
    '''
    Factory for messages
    '''
    FACTORY_FOR = Message

    message = lorem_ipsum()
    user = factory.SubFactory(UserFactory)
    messageType = factory.SubFactory(MessageTypeFactory)
    georegion = factory.SubFactory(RegionFactory)
    #location = factory.LazyAttribute(lambda n: point_gen(n))
    address = factory.Sequence(lambda n: "address string %s" % n)
