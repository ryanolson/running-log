# -*- coding: utf-8 -*-
"""
    running_log.forms
    ~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask.ext.wtf import Form
from flask_security.forms import RegisterForm
from wtforms.fields import TextField, BooleanField, IntegerField
from wtforms.fields import HiddenField, DateField
from wtforms.validators import Required, NumberRange, Optional

from .utils import is_date_editable, editable_range, flash_errors

from .runs.forms import *

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

