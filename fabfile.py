# coding: utf-8

from fabric.api import *


def test(app=''):
    command = "./manage.py test --settings=Rynda.settings.test %s" % app
    local(command)


def coverage():
    local("coverage run manage.py test --settings=Rynda.settings.test")
    local("coverage html")
    local("coverage report")


def server():
    local("./manage.py runserver --settings=Rynda.settings.local")


def stage():
    local("./manage.py runserver 0.0.0.0:8000 --settings=Rynda.settings.stage")
