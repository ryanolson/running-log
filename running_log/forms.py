# -*- coding: utf-8 -*-
"""
    forms.py
    ~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask.ext.wtf import Form
from flask_security.forms import RegisterForm
from wtforms.fields import TextField, BooleanField, IntegerField, SubmitField
from wtforms.validators import Required

class ExtendedRegisterForm(RegisterForm):
    first_name = TextField('First Name', [Required()])
    last_name = TextField('Last Name', [Required()])
    johnnie_cc = BooleanField()
    graduation_year = IntegerField()


class RunEntryForm(Form):
    miles = IntegerField('Miles', [Required()])
    submit = SubmitField('Save')
