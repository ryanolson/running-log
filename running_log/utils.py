# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import arrow
from models.sqlalchemy import Run

def now():
    return arrow.now('US/Central')

def eod():
    return now().ceil('day')

def start_of_this_week():                                                                                                                                                                                          
    """Sunday marks the start of the Tim Miles running calendar."""
    today = now().floor('day')
    if today.weekday() == 6:
        sunday = today
    else:
        sunday = today.replace(days=-today.isoweekday())
    return sunday

def this_week():
    start = start_of_this_week()
    return arrow.Arrow.range('day', start, start.replace(days=+6))

def last_week():
    start = start_of_this_week().replace(weeks=-1)
    return arrow.Arrow.range('day', start, start.replace(days=+6))

def editable_range():
    """Tuesday is the last day the previous week is editable."""
    end = arrow.utcnow().to('US/Central').ceil('day')
    start = start_of_this_week()
    if end.weekday() <= 1:
        start = start.replace(weeks=-1)
    return (start, end)

def is_date_editable(date):
    start, end = editable_range()
    if date <= end and date >= start:
        return True
    return False

def user_runs_between_dates(user, start, end):
    q = user.runs.filter(Run.date.between(start, end))
    q = q.order_by(Run.date)
    return q.all()

def user_runs_this_week(user):
    dates = this_week()
    start = dates[0]
    end = now()
    runs = user_runs_between_dates(user, start.date(), end.date())
    rundict = { date.format('YYYY-MM-DD'): None for date in dates if date <= end }
    for run in runs:
        date = arrow.Arrow.fromdate(run.date)
        rundict[date.format('YYYY-MM-DD')] = run
    return rundict

class Runs(object):

    def __init__(self, user, dates=None):
        if dates is None:
            dates = this_week()
        self.user = user
        self.dates = dates
        self.runs = user_runs_between_dates(user, dates[0].date(), dates[-1].date())
        self._hash_data()

    def _hash_data(self):
        self._data = { date.format('YYYY-MM-DD'): None for date in self.dates }
        for run in self.runs:
            date = arrow.Arrow.fromdate(run.date)
            self._data[date.format('YYYY-MM-DD')] = run

    @property
    def total_miles(self):
        return sum([run.miles for run in self.runs])

    def miles_for_date(self, date):
        if not isinstance(date, arrow.Arrow):
            raise TypeError
        if date < self.dates[0] or date > self.dates[-1]:
            raise ValueError
        run = self._data.get(date.format('YYYY-MM-DD'), None)
        if run:
            return run.miles
        return 0



