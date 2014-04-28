# -*- coding: utf-8 -*-
"""
    running_log.runs.services
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from ..core import SQLService
from ..models import Group, User

class GroupService(SQLService):
    __model__ = Group

    def add_user(self, group, user):
        if user in group.users:
            raise RunningLogError(u'User already exists in Group')
        group.users.append(user)
        return self.save(group), user

    def remove_user(self, group, user):
        if user not in group.users:
            raise RunningLogError(u'User not in Group; can not remove')
        group.users.remove(user)
        return self.save(group), user
