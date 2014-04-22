# -*- coding: utf-8 -*-
"""
    running_log.users.forms
    ~~~~~~~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask.ext.wtf import Form
from flask.ext.security.forms import RegisterForm
from wtforms.fields import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional

from .utils import flash_errors, is_date_editable, editable_range


class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    johnnie_cc = BooleanField('Johnnie CC', validators=[Optional()])
    graduation_year = SelectField('Gradutation Year',
            choices=[(year, str(year)) for year in range(1970,2018)],
            validators=[Optional()])


    def validate(self):
        rv = super(ExtendedRegisterForm, self).validate()
        if self.johnnie_cc and not bool(self.graduation_year):
            rv = False
            self.graduation_year.errors.append("Graduation Year required.")

        if not rv:
            flash_errors(self)

        return rv

