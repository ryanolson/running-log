# -*- coding: utf-8 -*-
"""
    running_log.forms
    ~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask.ext.wtf import Form
from flask.ext.security.forms import RegisterForm
from wtforms.fields import TextField, BooleanField, IntegerField
from wtforms.fields import HiddenField, DateField
from wtforms.validators import Required, NumberRange, Optional

from .runs.forms import *
from .utils import flash_errors

class ExtendedRegisterForm(RegisterForm):
    first_name = TextField('First Name', [Required()])
    last_name = TextField('Last Name', [Required()])
    johnnie_cc = BooleanField('Johnnie CC', [Optional()])
    graduation_year = IntegerField('Graduation Year', 
            validators=[Optional(), NumberRange(min=1970, max=2020)])

    def validate(self):
        rv = super(ExtendedRegisterForm, self).validate()
        if not rv:
            flash_errors(self)
        return rv

