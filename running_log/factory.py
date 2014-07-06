# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import os

from celery import Celery
from flask import Flask
from flask.ext.security import SQLAlchemyUserDatastore
from flask.ext.social import SQLAlchemyConnectionDatastore
from raven.contrib.flask import Sentry

from .core import db, mail, security, social
from .forms import ExtendedRegisterForm
from .helpers import register_blueprints
from .middleware import HTTPMethodOverrideMiddleware
from .models import User, Role, Connection


def create_app(package_name, package_path, settings_override=None,
               include_blueprints=True, register_security_blueprint=True):
    """
    Returns a :class:`Flask` application instance configured with common
    functionality for the RunningLog platform.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param register_security_blueprint: flag to specify if the Flask-Security
                                        Blueprint should be registered. Defaults
                                        to `True`.
    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('running_log.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    # Base Extensions
    db.init_app(app)
    mail.init_app(app)
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                      register_blueprint=register_security_blueprint,
                      register_form=ExtendedRegisterForm)
    social.init_app(app, SQLAlchemyConnectionDatastore(db, Connection))

    # Sentry - only for production 
    if not app.debug and not app.testing:
        sentry = Sentry(app)

    if include_blueprints:
        register_blueprints(app, package_name, package_path)

    # Middleware
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app


def create_celery_app(app=None):
    app = app or create_app('running_log', os.path.dirname(__file__),
            include_blueprints=False, register_security_blueprint=False)
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
