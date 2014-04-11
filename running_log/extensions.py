# -*- coding: utf-8 -*-
"""
    extensions.py
    ~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from clapp.extensions import *

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.security import Security
security = Security()

from flask.ext.social import Social
social = Social()

