import os

from fabric.api import *
from fabric.context_managers import prefix, cd, lcd, settings

from fabric.operations import local,  run
from fabric.api import task
from fabric.state import env

root_directory = os.path.join('~', 'Web', 'ProductionWebApps', 'RunningLog')
root_virtualenv = 'running-log'

dependencies = [
    'clapp',
]

@task
def localhost():
    env.cd = lcd
    env.run = local
    env.hosts = ['localhost']

@task
def remote():
    env.cd = cd
    env.run = run
    env.hosts = ['ryanolson.me']

@task
def restart():
    logs = os.path.join(root_directory, 'logs')
    with prefix('workon running-log'), env.cd(logs):
        env.run("ps aux | grep running_log")
        with settings(warn_only=True):
            env.run("../scripts/kill_gunicorn")
        env.run("gunicorn --daemon --name=running_log --pid=gunicorn.running-log.pid --bind 127.0.0.1:12346 --workers 4 running_log.application:create_app\(\)")
        env.run("ps aux | grep running_log")
        env.run("cat gunicorn.running-log.pid")

@task
def update():
    app_directory = os.path.join(root_directory, 'running-log')
    with env.cd(app_directory):
        env.run("git pull origin develop")
        env.run("git submodule update --init")
    with prefix('workon running-log'), env.cd(app_directory):
        env.run("python setup.py develop")

@task 
def copy_secrets():
    app_root_directory = os.path.join(root_directory, 'running-log', 'running_log')
    put('running_log/config_secret.py', app_root_directory)
