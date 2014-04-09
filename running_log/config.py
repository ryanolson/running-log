# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""

from . import config_social

class BaseConfig(object):

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = 'super-secret-key-errrr'

    # Flask-Bootstrap3
    USE_CDN = False

    # Flask-Security
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = True
    SECURITY_FLASH_MESSAGES = True
    SECURITY_POST_CONFIRM_VIEW = '/'
    SECURITY_POST_REGISTER_VIEW = '/'
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'it was in the spring of that year that i calibrated by stride'

    SOCIAL_CONNECT_ALLOW_VIEW = '/profile'
    SOCIAL_FACEBOOK = config_social.CONNECTIONS['facebook']
    SOCIAL_GITHUB = config_social.CONNECTIONS['github']
    SOCIAL_STRAVA = config_social.CONNECTIONS['strava']
    SOCIAL_APP_URL =  'https://tim-miles-running-log.com'

    # Sentry
    # SENTRY_DSN = 

    # Mixpanel
    # MIXPANEL_TOKEN = 

    # Babel
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'America/Denver'

class Production(BaseConfig):
    USE_CDN = True

    SQLALCHEMY_DATABASE_URI = "postgresql://ryan@127.0.0.1/running_log"

    COUCHDB_SERVER = "http://127.0.0.1:5984"
    COUCHDB_DATABASE = "running_log"

    MONGODB_DB = 'running_log'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

    LOG_FOLDER = '.'

class Debug(Production):
    DEBUG = True
    USE_CDN = False


class Config(Production):
    pass


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False
