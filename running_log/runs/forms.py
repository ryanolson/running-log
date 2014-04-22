# -*- coding: utf-8 -*-
"""
    running_log.runs.forms
    ~~~~~~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask.ext.wtf import Form
from flask.ext.security.forms import NextFormMixin
from wtforms.fields import IntegerField, HiddenField
from wtforms.validators import NumberRange

from .. import utils

class RunForm(NextFormMixin, Form):
    date = HiddenField()
    miles = IntegerField('Miles', 
            validators=[NumberRange(min=0, max=50)], default=0)

    def validate(self):
        if not super(RunForm, self).validate():
            return False
        date = utils.get_rldate(self.date.data)
        if not utils.is_date_editable(date):
            self.date.errors.append('{0} is not editable'.format(
                date.format('M/D/YY')))
            return False
        return True 

    def to_dict(self):
        return dict(miles=self.miles.data, date=self.date.data)
