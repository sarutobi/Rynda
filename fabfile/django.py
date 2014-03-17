# -*- coding: utf-8 -*-

from fabric.api import *


def syncdb(settings):
    run("django-admin.py syncdb --settings=%s" % settings)


def migrate_db(settings):
    run("django-admin.py migrate --settings=%s" % settings)


@task
def update_database(settings):
    syncdb(settings)
    migrate_db(settings)


@task
def collectstatic(settings):
    run("django-admin.py collectstatic --settings=%s" % settings)
