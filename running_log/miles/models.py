# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from sqlalchemy import or_, and_

from . import extensions
from .. import rl_arrow
from ..models.sqlalchemy import User, Run


class UserRuns(object):

    def __init__(self, user, dates=None, start_date=None, end_date=None):
        now = rl_arrow.now()
        if dates is None:
            dates = now.this_week
        self._user = user
        self._start_date = start_date or dates[0]
        self._end_date = end_date or dates[-1]
        self._runs = self.runs_between(self._user, self._start_date.date(),
                self._end_date.date())
        datestr = lambda x: rl_arrow.fromdate(x).format('YYYY-MM-DD')
        self._data = { datestr(run.date): run for run in self._run }

    @property
    def user(self):
        return self._user

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def dates(self):
        return rl_arrow.RLArrow.range('day', self._state_date, self._end_date)

    @property
    def runs(self):
        return self._runs

    @property
    def total_miles(self):
        return sum([run.miles for run in self.runs])

    @classmethod
    def runs_between(user, start_date, end_date):
        query = user.runs.\
                filter(Run.date.between(start_date, end_date)).\
                order_by(Run.date)
        return query.all()

    def miles_for_date(self, date):
        if isinstance(date, basestring):
            date = rl_arrow.get(date, 'YYYY-MM-DD')
        elif isinstance(date, datetime.date):
            date = rl_arrow.fromdate(date)
        elif isinstance(date, arrow.Arrow):
            pass
        else:
            raise TypeError('unrecognized date = {0}'.format(str(date)))
        if date < self.start_date or date > self.end_date:
            raise ValueError('the requested date is out-of-range')
        run = self._data.get(date.format('YYYY-MM-DD'), None)
        if run:
            return run.miles
        return 0

