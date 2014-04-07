# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import pytest
import datetime
from running_log import rl_arrow

class TestRLArrow:

    def test_weekday(self):
        now = rl_arrow.now()
        print now.weekday()

    def test_print(self):
        now = rl_arrow.now()
        print "now = {}",format(now)
        print "sod = {}".format(now.sod)
        print "eod = {}".format(now.eod)
        print "sow = {}".format(now.sow)
        print "eow = {}".format(now.eow)
        for day in now.this_week:
            print day, day.weekday()
        fd = rl_arrow.fromdate(datetime.date(2014,02,20))
        print fd
        fs = rl_arrow.fromstr('2014-02-20')
        print fs
        print fs.datestr
