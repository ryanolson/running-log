# -*- coding: utf-8 -*-
"""
    running_log.groups.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from .. import helpers
from ..core import db


groups_users = db.Table('groups_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('groups.id')))


class GroupJsonSerializer(helpers.JsonSerializer):
    pass


class Group(GroupJsonSerializer, db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(255))

    users = db.relationship('User', secondary=groups_users, 
            backref=db.backref('groups', lazy='dynamic'))
