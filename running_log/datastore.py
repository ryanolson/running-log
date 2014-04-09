# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask.ext.security.datastore import SQLAlchemyDatastore

from . import utils

class RunningLogDatastore(object):

    def __init__(self, user, run, group):
        self.user_model = user
        self.run_model = run
        self.group_model = group
   
    def create_group(self, **kwargs):
        group = self.group_model(**kwargs)
        return self.put(group)

    def find_group(self, *args, **kwargs):
        raise NotImplementedError

    def find_or_create_group(self, name, **kwargs):
        """Returns a group matching the given name or creates it with any
        additionally provided parameters
        """
        kwargs["name"] = name
        return self.find_group(name) or self.create_group(**kwargs)

    def add_user_to_group(self, user, group):
        raise NotImplementedError

    def remove_user_from_group(self, user, group):
        raise NotImplementedError

    def set_primary_group_for_user(self, user, group):
        raise NotImplementedError

    def user_runs(self, user, start_date=None, end_date=None):
        raise NotImplementedError

    def group_runs(self, group, start_date=None, end_date=None):
        raise NotImplementedError

    def johnnie_cc_runs(self, user, start_date=None, end_date=None):
        raise NotImplementedError

class SQLAlchemyRunningLogDatastore(SQLAlchemyDatastore, RunningLogDatastore):

    def __init__(self, db, user, run, group):
        SQLAlchemyDatastore.__init__(self, db)
        RunningLogDatastore.__init__(self, user, run, group)

    def append_date_filter(self, query, field, start_date=None, end_date=None):
        start = utils.get_rldate(start_date)
        end = utils.get_rldate(end_date)
        if start_date and end_date:
            return query.filter(field.between(start.date(), end.date()))
        if start_date:
            return query.filter(field >= start_date)
        if end_date:
            return query.filter(field <= end_date)
        return query

    def user_runs(self, user, start_date, end_date):
        start = utils.get_rldate(start_date)
        end = utils.get_rldate(end_date)
        query = self.append_date_filter(user.runs, self.run_model.date,
                start_date=start_date, end_date=end_date)
        return query.all()

    def johnnie_cc_runs(self, user, start_date=None, end_date=None):
        query = self.run_model.query.join(self.user_model).\
                filter(self.user_model.johnnie_cc == True)
        query = self.append_date_filter(query, self.run_model.date,
                start_date=start_date, end_date=end_date)
        return query.all()
