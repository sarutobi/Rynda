# coding: utf-8

from fabric.api import *

REQUIREMENT_SET = {
    'base': 'Rynda/requirements/_base.txt',
    'ci': 'Rynda/requirements/ci.txt',
    'dev': 'Rynda/requirements/develop.txt',
    'prod': 'Rynda/requirements/production.txt',
    'test': 'Rynda/requirement/test.txt',
}


def test(app=''):
    command = "./manage.py test --settings=Rynda.settings.test %s" % app
    local(command)


def coverage():
    local("coverage run manage.py test --settings=Rynda.settings.test")
    local("coverage html")
    local("coverage report")


def server():
    local("./manage.py runserver --settings=Rynda.settings.local")


def local_stage():
    local("./manage.py runserver 0.0.0.0:8000 --settings=Rynda.settings.local_stage")


def requirements(settings='base'):
    req = REQUIREMENT_SET.get(settings, REQUIREMENT_SET.get('base'))
    local('pip install -r %s' % req)
