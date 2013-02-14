# coding: utf-8

from fabric.api import *


def test():
    local("./manage.py test --settings=Rynda.settings.test")


def coverage():
    local("coverage run manage.py test --settings=Rynda.settings.test")
    local("coverage html")
    local("coverage report")


def server():
    local("./manage.py runserver --settings=Rynda.settings.local")
