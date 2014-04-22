# -*- coding: utf-8 -*-
"""
    running_log.settings
    ~~~~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""

# Flask
DEBUG = True
TESTING = False

# Database / Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = "postgresql://ryan@127.0.0.1/running_log"

# Flask-Bootstrap3
USE_CDN = True

# Flask-Mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'tim.miles.running.log@gmail.com'

# Flask-Security
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_TRACKABLE = True
SECURITY_FLASH_MESSAGES = True
SECURITY_POST_CONFIRM_VIEW = '/'
SECURITY_POST_REGISTER_VIEW = '/'
SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_EMAIL_SENDER = 'tim.miles.running.log@gmail.com'

# Flask-Social
SOCIAL_CONNECT_ALLOW_VIEW = '/profile'
SOCIAL_APP_URL =  'https://tim-miles-running-log.com'

# Babel
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'America/Denver'

