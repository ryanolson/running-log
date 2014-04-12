# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""

from . import config_secret

class BaseConfig(object):

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = config_secret.SECRET_KEY

    # Flask-Bootstrap3
    USE_CDN = False

    # Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'tim.miles.running.log@gmail.com'
    MAIL_PASSWORD = config_secret.MAIL_PASSWORD

    # Flask-Security
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_FLASH_MESSAGES = True
    SECURITY_POST_CONFIRM_VIEW = '/'
    SECURITY_POST_REGISTER_VIEW = '/'
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_EMAIL_SENDER = 'tim.miles.running.log@gmail.com'

    SECURITY_PASSWORD_SALT = config_secret.SECURITY_PASSWORD_SALT
    SECURITY_CONFIRM_SALT = config_secret.SECURITY_CONFIRM_SALT
    SECURITY_RESET_SALT = config_secret.SECURITY_RESET_SALT
    SECURITY_LOGIN_SALT = config_secret.SECURITY_LOGIN_SALT
    SECURITY_REMEMBER_SALT = config_secret.SECURITY_REMEMBER_SALT


    SOCIAL_CONNECT_ALLOW_VIEW = '/profile'
    SOCIAL_FACEBOOK = config_secret.CONNECTIONS['facebook']
    SOCIAL_GITHUB = config_secret.CONNECTIONS['github']
    SOCIAL_STRAVA = config_secret.CONNECTIONS['strava']
    SOCIAL_APP_URL =  'https://tim-miles-running-log.com'

    # Sentry
    SENTRY_DSN = config_secret.SENTRY_DSN

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
