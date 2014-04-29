# -*- coding: utf-8 -*-
"""
    running_log.runs.models
    ~~~~~~~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import collections
from copy import copy

from .. import helpers
from .. import utils
from ..core import db


class RunJsonSerializer(helpers.JsonSerializer):
    pass


class Run(RunJsonSerializer, db.Model):
    __tablename__ = "runs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    miles = db.Column(db.Integer)
#   details = relationship("RunDetails", uselist=False, backref="run")


class RunDetailsJsonSerializer(helpers.JsonSerializer):
    pass


class RunDetails(RunJsonSerializer, db.Model):
    __tablename__ = "rundetails"

    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey('runs.id'))
    link = db.Column(db.String(510))



class Runs(object):

    def __init__(self, runs=None):
        self._runs = runs or []
        self._runs_by_date = collections.defaultdict(list)
        for run in self._runs:
            self.add_run(run)

    @property
    def runs(self):
        return self._runs

    @property
    def total_miles(self):
        return sum([run.miles for run in self._runs])

    def add_run(self, run):
        date = utils.get_rldate(run.date)
        self._runs_by_date[date.ymd].append(run)

    def runs_for_date(self, date):
        date = utils.get_rldate(date)
        if date.ymd in self._runs_by_date:
            return copy(self._runs_by_date[date.ymd])
        return []

    def miles_for_date(self, date):
        return sum([run.miles for run in self.runs_for_date(date)])

    def miles_over_range(self, dates):
        return sum([self.miles_for_date(date) for date in dates])


class UserRuns(Runs):

    def __init__(self, user=None, runs=None):
        super(UserRuns, self).__init__(runs)
        self.set_user(user)

    @property
    def user(self):
        return self._user

    def set_user(self, user):
        self._user = user


class GroupRuns(Runs):

    def __init__(self, runs=None):
        self._runs_by_user = collections.defaultdict(UserRuns)
        super(GroupRuns, self).__init__(runs)

    def _user_key(self, user):
        return "{0}, {1}".format(user.last_name, user.first_name)

    @property
    def runs_by_user(self):
        return copy(self._runs_by_user)

    @property 
    def user_keys(self):
        return sorted(self._runs_by_user.iterkeys())

    def add_run(self, run):
        super(GroupRuns, self).add_run(run)
        key = self._user_key(run.user)
        self._runs_by_user[key].set_user(run.user)
        self._runs_by_user[key].add_run(run)


class CCRuns(GroupRuns):

    def __init__(self, runs=None):
        self._users_by_year = collections.defaultdict(set)
        super(CCRuns, self).__init__(runs)

    @property
    def users_by_year(self):
        return self._users_by_year

    def add_run(self, run):
        super(CCRuns, self).add_run(run)
        key = self._user_key(run.user)
        self._users_by_year[str(run.user.graduation_year)].add(key)

