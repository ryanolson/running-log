# -*- coding: utf-8 -*-
"""
    tests.factories
    ~~~~~~~~~~~~~~~

    RunningLog test factories module
"""

from datetime import datetime

from factory import Factory, Sequence, LazyAttribute
from flask_security.utils import encrypt_password

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
    email = Sequence(lambda n: 'user{0}@running_log.com'.format(n))
    password = LazyAttribute(lambda a: encrypt_password('password'))
    last_login_at = datetime.utcnow()
    current_login_at = datetime.utcnow()
    last_login_ip = '127.0.0.1'
    current_login_ip = '127.0.0.1'
    login_count = 1
    roles = LazyAttribute(lambda _: [RoleFactory()])
    active = True

