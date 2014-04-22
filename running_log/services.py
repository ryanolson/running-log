# -*- coding: utf-8 -*-
"""
    running_log.services
    ~~~~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from .runs import RunService
from .users import UserService

#: An instance of the :class:`UserService` class
users = UserService()

#: An instance of the :class:`RunService` class
runs = RunService()

