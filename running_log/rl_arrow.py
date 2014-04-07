# -*- coding: utf-8 -*-                                                                                                                                                                                            
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from __future__ import absolute_import

import arrow


class RLArrow(arrow.Arrow):
    """Custom Arrow class."""

    def weekday(self):
        """Running Log starts on Sunday; adjust weekday to match."""
        return (super(RLArrow, self).weekday() + 1) % 7

    @property
    def sod(self):
        """Start of day"""
        return self.floor('day')

    @property
    def eod(self):
        """End of day"""
        return self.ceil('day')

    @property
    def sow(self):
        """Start of week"""
        sunday = self
        if self.weekday():
            sunday = self.replace(days=-today.isoweekday())
        return sunday.floor('day') 

    @property
    def eow(self):
        """Start of week"""
        return self.eod.replace(days=+6).ceil('day')

    @property
    def this_week(self):
        """List of days in the week"""
        return self.range('day', self.sow, self.eow)

    @property
    def last_week(self):
        """List of days in the previous week"""
        return self.replace(weeks=-1).this_week

    @property
    def datestr(self):
        return self.format('YYYY-MM-DD')


# Internal Factory
_factory = arrow.ArrowFactory(RLArrow)


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
    return RLArrow.fromdate(date).replace(tzinfo='US/Central')


def fromstr(date, format='YYYY-MM-DD'):
    return _factory.get(date, format).replace(tzinfo='US/Central')

__all__ = ['get', 'utcnow', 'now', 'fromdate']
