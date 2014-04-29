# -*- coding: utf-8 -*-
"""
    tests.factories
    ~~~~~~~~~~~~~~~

    RunningLog test factories module
"""

from datetime import datetime

from factory import Factory, Sequence, LazyAttribute
from factory import fuzzy
from flask_security.utils import encrypt_password

from running_log import rltime
from running_log.core import db
from running_log.models import *

class BaseFactory(Factory):
    ABSTRACT_FACTORY = True

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        entity = target_class(**kwargs)
        db.session.add(entity)
        db.session.commit()
        return entity


class RoleFactory(BaseFactory):
    FACTORY_FOR = Role
    name = 'admin'
    description = 'Administrator'


class UserFactory(BaseFactory):
    FACTORY_FOR = User
    first_name = fuzzy.FuzzyChoice(['Ryan', 'Mike', 'Paul', 'Rob', 'Lars'])
    last_name = fuzzy.FuzzyChoice(['Olson', 'Cook', 'Kleinschmidt', 'Zelada', 'Liepold'])
    email = Sequence(lambda n: 'user{0}@running_log.com'.format(n))
    password = LazyAttribute(lambda a: encrypt_password('password'))
    confirmed_at = datetime.utcnow()
    last_login_at = datetime.utcnow()
    current_login_at = datetime.utcnow()
    last_login_ip = '127.0.0.1'
    current_login_ip = '127.0.0.1'
    login_count = 1
    #roles = LazyAttribute(lambda _: [RoleFactory()])
    groups = LazyAttribute(lambda _: [GroupFactory()])
    active = True

class RunFactory(BaseFactory):
    FACTORY_FOR = Run
    miles = fuzzy.FuzzyInteger(0, 10)


class UserWithRunsFactory(UserFactory):

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        entity = target_class(**kwargs)
        for day in rltime.RLTime.range('day', *utils.editable_range()):
            entity.runs.append(RunFactory(date=day.date()))
        db.session.add(entity)
        db.session.commit()
        return entity


class GroupFactory(BaseFactory):
    FACTORY_FOR = Group
    name = Sequence(lambda n: 'group{0}'.format(n))
