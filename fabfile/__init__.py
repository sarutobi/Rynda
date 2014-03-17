# coding: utf-8

from fabric.api import *

import django
import git
import local

# Localhost virtualenvwrapper activation
LOCAL_VIRT_ACTIVATE = 'source ~/.zshrc'

# Project settings
VIRT_COMMAND = 'workon rynda'

REQUIREMENT_SET = {
    'base': 'Rynda/requirements/_base.txt',
    'ci': 'Rynda/requirements/ci.txt',
    'dev': 'Rynda/requirements/develop.txt',
    'prod': 'Rynda/requirements/production.txt',
    'test': 'Rynda/requirement/test.txt',
}


def coverage():
    local("coverage run manage.py test --settings=Rynda.settings.test")
    local("coverage html")
    local("coverage report")


def server():
    local("./manage.py runserver --settings=Rynda.settings.local")


@task
def upgrade():
    git.push()
    CONTEXT_PATH = prompt("Путь к корневой директории: ")
    CONTEXT_USER = prompt("Имя пользователя: ")
    CONTEXT_SETTINGS = prompt("Файл настроек: ")
    with cd(CONTEXT_PATH), settings(sudo_user=CONTEXT_USER):
        git.pull()
        django.update_database(CONTEXT_SETTINGS)
