# -*- coding: utf-8 -*-                                                                                                                                                                                            
"""
    running_log.rltime
    ~~~~~~~~~~~~~~~~~~

    Customized Arrow for RunningLog.

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from __future__ import absolute_import

import arrow


class RLTime(arrow.Arrow):
    """Custom Arrow class."""

    def weekday(self):
        """Running Log starts on Sunday; adjust weekday to match."""
        return (super(RLTime, self).weekday() + 1) % 7

    def isoweekday(self):
        """Running Log starts on Sunday; adjust weekday to match."""
        return self.weekday() + 1

    @property
    def this_week(self):
        """List of days in the week"""
        start, end = self.span('week')
        return self.range('day', start, end)

    @property
    def last_week(self):
        """List of days in the previous week"""
        return self.replace(weeks=-1).this_week

    @property
    def ymd(self):
        return self.format('YYYY-MM-DD')

    @property
    def md(self):
        return self.format('M/D')


# Internal Factory
_factory = arrow.ArrowFactory(RLTime)


# API

def get(*args, **kwargs):
    ''' Implements the default :class:`ArrowFactory <arrow.factory.ArrowFactory>`
    ``get`` method.

    '''
    if 'tzinfo' not in kwargs:
        kwargs['tzinfo'] = 'US/Central'
    return _factory.get(*args, **kwargs)

def utcnow():
    ''' Implements the default :class:`ArrowFactory <arrow.factory.ArrowFactory>`
    ``utcnow`` method.

    '''

    return _factory.utcnow()


def now(tz='US/Central'):
    ''' Implements the default :class:`ArrowFactory <arrow.factory.ArrowFactory>`
    ``now`` method.

    '''

    return _factory.now(tz)

def fromdate(date):
    return RLTime.fromdate(date).replace(tzinfo='US/Central')


def fromstr(date, format='YYYY-MM-DD'):
    return _factory.get(date, format).replace(tzinfo='US/Central')

__all__ = ['get', 'utcnow', 'now', 'fromdate']
