# -*- coding: utf-8 -*-

from fabric.api import *

import fabfile

# Localhost virtualenvwrapper activation
LOCAL_VIRT_ACTIVATE = 'source ~/.zshrc'

# Project settings
VIRT_COMMAND = 'workon rynda'


@task
def server():
    with prefix(LOCAL_VIRT_ACTIVATE), prefix(VIRT_COMMAND):
        local("./manage.py runserver --settings=Rynda.settings.local")


@task
def test(app=''):
    with prefix(LOCAL_VIRT_ACTIVATE), prefix(VIRT_COMMAND):
        command = "./manage.py test --settings=Rynda.settings.test %s" % app
        local(command, shell='/bin/zsh')


@task
def requirements(settings='base'):
    req = fabfile.REQUIREMENT_SET.get(settings, fabfile.REQUIREMENT_SET.get('base'))
    with prefix(LOCAL_VIRT_ACTIVATE), prefix(VIRT_COMMAND):
        local('pip install -r %s' % req, shell='/bin/zsh')


@task
def stage():
    with prefix(LOCAL_VIRT_ACTIVATE), prefix(VIRT_COMMAND):
        local("./manage.py runserver 0.0.0.0:8000 --settings=Rynda.settings.local_stage")
