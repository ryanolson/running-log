# -*- coding: utf-8 -*-
"""
    forms.py
    ~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import arrow
from clapp.forms import flash_errors
from flask.ext.wtf import Form
from flask_security.forms import RegisterForm, NextFormMixin
from wtforms.fields import TextField, BooleanField, IntegerField, SubmitField
from wtforms.fields import HiddenField, DateField
from wtforms.validators import Required, NumberRange, Optional

from .utils import is_date_editable, editable_range


class ExtendedRegisterForm(RegisterForm):
    first_name = TextField('First Name', [Required()])
    last_name = TextField('Last Name', [Required()])
    johnnie_cc = BooleanField('Johnnie CC', [Optional()])
    graduation_year = IntegerField('Graduation Year', [Optional()])

    def validate(self):
        rv = super(ExtendedRegisterForm, self).validate()
        if not rv:
            flash_errors(self)
        return rv

class RunEntryForm(Form, NextFormMixin):
    date = HiddenField()
    miles = IntegerField('Miles', [NumberRange(min=0, max=50)], default=0)
    submit = SubmitField('Save')

    def validate(self):
        if not super(RunEntryForm, self).validate():
            return False

        date = arrow.get(self.date.data, 'YYYY-MM-DD').replace(tzinfo="US/Central")
        if not is_date_editable(date):
            self.date.errors.append('{0} is not editable'.format(
                date.format('M/D/YY')))
            return False
        
        return True

    def to_dict(self):
        return dict(miles=self.miles.data, date=self.date.data)
