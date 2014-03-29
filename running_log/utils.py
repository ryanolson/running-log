# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import arrow

def start_of_this_week():                                                                                                                                                                                          
    """Sunday marks the start of the Tim Miles running calendar."""
    today = arrow.utcnow().to('America/Chicago').floor('day')
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
    end = arrow.utcnow().to('America/Chicago').ceil('day')
    start = start_of_this_week()
    if end.weekday() <= 1:
        start.replace(weeks=-1)
    return (start, end)

def is_date_editable(date):
    start, end = editable_range()
    if date < end and date >= start:
        return True
    return False

def date_from_string(date_str):
    return arrow.get(date_str, 'M/D/YY')
