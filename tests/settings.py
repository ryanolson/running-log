# -*- coding: utf-8 -*-
"""
    tests.settings
    ~~~~~~~~~~~~~~

    tests settings module
"""

DEBUG = False
TESTING = True
SECRET_KEY = 'testing-secret-key'

SQLALCHEMY_POOL_SIZE = None
SQLALCHEMY_POOL_TIMEOUT = None
SQLALCHEMY_POOL_RECYCLE = None
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

SECURITY_PASSWORD_HASH = 'plaintext'

WTF_CSRF_ENABLED = False
