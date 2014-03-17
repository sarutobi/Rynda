# -*- coding: utf-8 -*-

from fabric.api import local, run, task


@task
def pull(branch="master"):
    run('git pull %s' % branch)


@task
def push(branch="master"):
    local("git push")
