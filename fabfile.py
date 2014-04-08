from fabric.api import *
from fabric.context_managers import prefix, cd


env.hosts = ['ryanolson.me']

root_dir = os.path.join('Web', 'RunningLog')
virtualenv = 'running-log'

dependencies = [
    'clapp',
]

def load_virtualenv(branch):
    return "workon {0}.{1}".format(virtualenv, branch)

def deploy(branch='develop', deploy_dir=None):
    deploy_dir = os.path.join(root_dir, branch)
    local("git push origin {0}".format(branch))
    with cd(deploy_dir):
        run("git pull origin {0}".format(branch))
        run("git submodule update --init");
        with prefix(load_virtualenv(branch)):
            for dependence in dependencies:
                with cd("dependencies/{0}".format(dependence)):
                    run("python setup.py develop")
            run("python setup.py develop")
    with prefix(load_virtualenv(branch)):
        run("pkill gunicorn; gunicorn --daemon --bind 127.0.0.1:12345 --workers 4 benchmarkr.application:create_app\(\)")
    with prefix("workon {0}".format(virtualenv)), cd("{0}/logs/celery".format(srcdir)):
        run("celeryd-multi restart benchmarkr1 --app=benchmarkr.worker --autoreload --concurrency=2 --loglevel=info")

def initialize(branch='develop'):
    pass

def clean(branch='develop')
    pass

def restart_celery():
    with prefix("workon Benchmarkr"), cd("/usr/local/var/www/benchmarkr/logs"):
        run("celeryd-multi restart benchmarkr1 --app=benchmarkr.worker --autoreload --concurrency=2 --loglevel=info")
