# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import arrow
import datetime
import hashlib
import urllib

from . import rltime

def get_rldate(date):
    """Converts multiple forms of a date to a rltime object."""
    if date is None:
        return None
    if isinstance(date, rltime.RLTime):
        pass
    elif isinstance(date, basestring):
        date = rltime.fromstr(date)
    elif isinstance(date, datetime.date):
        date = rltime.fromdate(date)
    elif isinstance(date, arrow.Arrow):
        date = rltime.fromdate(data.date())
    else:
        raise TypeError('unrecognized date = {0}'.format(str(date))) 
    return date

def gravatar_url(email, size=300):
    url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    url += urllib.urlencode({'d':'mm', 's':str(size)})
    return url

def editable_range():
    """Tuesday is the last day the previous week is editable."""
    now = rltime.now()
    start, end = now.span('week')[0], now.ceil('day')
    if end.weekday() <= 2:
        start = start.replace(weeks=-1)
    return (start, end)

def is_date_editable(date):
    start, end = editable_range()
    if date <= end and date >= start:
        return True
    return False
