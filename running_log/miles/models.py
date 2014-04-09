# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import collections

from copy import copy
from flask import current_app
from werkzeug.local import LocalProxy

from .. import rltime
from .. import utils

_running_log = LocalProxy(lambda: current_app.extensions['running_log'])
_datastore = LocalProxy(lambda: _running_log.datastore)

_datestr = lambda date: rltime.fromdate(date).ymd

class RunsByDate(object):

    def __init__(self, runs=None, start_date=None, end_date=None):
        self._start_date = utils.get_rldate(start_date)
        self._end_date = utils.get_rldate(end_date)
        self._runs = runs or []
        self._runs_by_date = collections.defaultdict(list)
        for run in self._runs:
            self.add_run(run)

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def dates(self):
        if self.start_date and self.end_date:
            return rltime.RLArrow.range('day', self._state_date, self._end_date)
        return []

    @property
    def runs(self):
        return self._runs

    @property
    def total_miles(self):
        return sum([run.miles for run in self._runs])

    def validate_date(self, date):
        date = utils.get_rldate(date)
        if date < self._start_date or date > self._end_date:
            raise ValueError('run not in date range')
        return date

    def add_run(self, run):
        date = self.validate_date(run.date)
        self._runs_by_date[date.ymd].append(run)

    def runs_for_date(self, date):
        date = self.validate_date(date)
        if date.ymd in self._runs_by_date:
            return copy(self._runs_by_date[date.ymd])
        return None

    def miles_for_date(self, date):
        runs = self.runs_for_date(date)
        if runs:
            return sum([run.miles for run in runs])
        return 0

    def miles_over_range(self, dates):
        return sum([self.miles_for_date(date) for date in dates])


class UserRunsByDate(RunsByDate):

    def __init__(self, user=None, runs=None, start_date=None, end_date=None):
        RunsByDate.__init__(self, runs=runs, start_date=start_date, end_date=end_date)
        self.user = user


class GroupRunsByDate(RunsByDate):

    def __init__(self, runs=None, start_date=None, end_date=None):
        super(GroupRunsByDate, self).__init__(runs=runs, start_date=start_date, end_date=end_date)
        self._runs_by_user = collections.defaultdict(UserRunsByDate)

    @property 
    def user_keys(self):
        return sorted(self._runs_by_user.iterkeys())

    def add_run(self, run):
        super(GroupRunsByDate, self).add_run(run)
        key = "{0}, {1}".format(run.user.last_name, run.user.first_name)
        self._runs_by_user[key].user = run.user
        self._runs_by_user[key].add_run(run)


class DefaultToThisWeek(object):
    
    def __init__(self, start_date=None, end_date=None):
        start_of_week, end_of_week = rltime.now().span('week')
        self._start_date = utils.get_rldate(start_date) or start_of_week
        self._end_date = utils.get_rldate(end_date) or end_of_week


class UserRuns(UserRunsByDate, DefaultToThisWeek):

    def __init__(self, user, start_date=None, end_date=None):
        UserRunsByDate.__init__(self, user=user, runs=None, start_date=start_date, end_date=end_date)
        DefaultToThisWeek.__init__(self, start_date=start_date, end_date=end_date)
        runs = _datastore.user_runs(user, self.start_date, self.end_date)
        for run in runs:
            self.add_run(run)


class GroupRuns(GroupRunsByDate, DefaultToThisWeek):

    def __init__(self, group, start_date=None, end_date=None):
        GroupRunsByDate.__init(self, start_date=start_date, end_date=end_data)
        DefaultToThisWeek.__init__(self, start_date=start_date, end_date=end_date)
        runs = _datastore.group_runs(group, self.start_date, self.end_date)
        for run in runs:
            self.add_run(run)


class JohnnieCCRuns(GroupRunsByDate, DefaultToThisWeek):

    def __init__(self, user, start_date=None, end_date=None):
        GroupRunsByDate.__init__(self, start_date=start_date, end_date=end_date)
        DefaultToThisWeek.__init__(self, start_date=start_date, end_date=end_date)
        runs = _datastore.johnnie_cc_runs(user, self.start_date, self.end_date)
        for run in runs:
            self.add_run(run)


