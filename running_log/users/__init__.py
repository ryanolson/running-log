# -*- coding: utf-8 -*-
"""
    running_log.users
    ~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from ..core import SQLService
from .models import User

from . import models

class UserService(SQLService):
    __model__ = User
