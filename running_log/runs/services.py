# -*- coding: utf-8 -*-
"""
    running_log.runs.services
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from ..core import SQLService
from ..utils import date_filter, get_rldate
from ..models import Run, User, UserRuns, GroupRuns, CCRuns

class RunService(SQLService):
    __model__ = Run

    def find_runs_for_user(self, user, start_date, end_date):
        return date_filter(user.runs, Run.date, start_date, end_date)

    def find_runs_for_group(self, group, start_date, end_date):
        raise NotImplementedError

    def find_runs_for_johnnie_cc(self, user, start_date, end_date, all_years=False):
        q = date_filter(Run.query, Run.date, start_date, end_date)
        q = q.join(User).filter(User.johnnie_cc == True)
        if not all_years:
            q = q.\
                    filter(User.graduation_year >= user.graduation_year - 3).\
                    filter(User.graduation_year <= user.graduation_year + 3)
        return q

    def get_user_runs(self, user, start_date, end_date):
        runs = self.find_runs_for_user(user, start_date, end_date).all()
        return UserRuns(user=user, runs=runs)

    def get_group_runs(self, group, start_date, end_date):
        raise NotImplementedError

    def get_cc_runs(self, user, start_date, end_date, all_years=False):
        runs = self.find_runs_for_johnnie_cc(user, start_date, end_date, 
                all_years=all_years).all() if user.johnnie_cc else []
        return CCRuns(runs=runs)

    def update_run(self, user, date, miles):
        date = get_rldate(date)
        run = self.first(date=date.date(), user_id=user.id)
        if run is None:
            run = self.new(user_id=user.id, date=date.date())
        run.miles = miles
        self.save(run)

