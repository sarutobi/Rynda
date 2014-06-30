# -*- coding: utf-8 -*-

import factory
from factory import django, fuzzy
from test.factories import UserFactory
from test.utils import FuzzyText

from geozones.factories import LocationFactory
from core.factories import SubdomainFactory
from .models import Message


class MessageFactory(django.DjangoModelFactory):
    """ Factory for messages. """
    FACTORY_FOR = Message

    title = FuzzyText()
    message = FuzzyText(length=200)
    messageType = fuzzy.FuzzyChoice(
        (Message.REQUEST, Message.OFFER, Message.INFO))
    subdomain = factory.SubFactory(SubdomainFactory)
    # category = factory.SubFactory(CategoryFactory)
    is_anonymous = True
    allow_feedback = True
    is_virtual = fuzzy.FuzzyChoice((True, False))
    user = factory.SubFactory(UserFactory)
    source = fuzzy.FuzzyChoice(("", FuzzyText()))
    is_active = False
    is_important = False
    is_removed = False
    status = Message.NEW

    @factory.lazy_attribute
    def linked_location(self):
        if self.is_virtual:
            ret = None
        else:
            ret = LocationFactory()
        return ret

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for cat in extracted:
                self.category.add(cat)
