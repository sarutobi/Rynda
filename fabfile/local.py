# -*- coding: utf-8 -*-

from functools import wraps

from fabric.api import *

import fabfile

# Localhost virtualenvwrapper activation
LOCAL_VIRT_ACTIVATE = 'source ~/.zshrc'

# Project settings
VIRT_COMMAND = 'workon rynda'


def inside_virtualenv(func):
    """ Decorator for virtualenv """
    @wraps(func)
    def inner(*args, **kwargs):
        with prefix(LOCAL_VIRT_ACTIVATE), prefix(VIRT_COMMAND):
            return func(*args, **kwargs)
    return inner


@task
def manage(command='help'):
    local("python manage.py " + command, shell='/bin/zsh')


@task
@inside_virtualenv
def server():
    manage("runserver --settings=Rynda.settings.local")


@task
@inside_virtualenv
def test(app=''):
    command = "test --settings=Rynda.settings.test %s" % app
    manage(command)


@task
def pip(req_file='', upgrade=False):
    if upgrade:
        key = "-U"
    else:
        key = ""
    command = 'pip install -r %(file)s %(key)s' % {'file': req_file, 'key': key}
    local(command, shell='/bin/zsh')


@task
@inside_virtualenv
def install_req(req_file='', upgrade=False):
    pip(req_file, upgrade)


@task
def stage():
    manage("runserver 0.0.0.0:8000 --settings=Rynda.settings.local_stage")
