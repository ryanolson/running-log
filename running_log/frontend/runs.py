# -*- coding: utf-8 -*-
"""
    views.py
    ~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask import Blueprint, render_template, request, url_for
from flask.ext.security import current_user

from . import route
from .. import forms
from .. import rltime
from .. import services
from .. import utils

# Blueprint
bp = Blueprint('runs', __name__, url_prefix='/runs')


@route(bp, '/')
def index():
    now = rltime.now().floor('day')
    this_week, last_week = now.this_week, now.last_week
    start, end = last_week[0], this_week[-1]

    return render_template('runs/index.html', 
            now=now, this_week=this_week, last_week=last_week,
            runs=services.runs.get_user_runs(current_user, start, end),
            group_runs=None,
            cc_runs=services.runs.get_cc_runs(current_user, start, end))


@route(bp, '/update', methods=['GET', 'POST'])
def update():
    form_class = forms.RunForm

    if request.form:
        form = form_class(request.form)
    else:
        form = form_class()

    if form.validate_on_submit():
        form.next.data = url_for('.index')
        services.runs.update_run(current_user, form.date.data, form.miles.data)
    else:
        print "errors"
        utils.flash_errors(form)

    return render_template('runs/run_form.html', run_form=form)


