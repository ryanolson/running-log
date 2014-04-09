# -*- coding: utf-8 -*-
"""
    views.py
    ~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from clapp.forms import flash_errors
from flask import Blueprint, render_template, current_app, \
        request, url_for
from flask.ext.login import login_required
from flask.ext.security import current_user
from werkzeug.local import LocalProxy

from . import models
from .. import forms
from .. import rltime
from .. import utils

_running_log = LocalProxy(lambda: current_app.extensions['running_log'])
_datastore = LocalProxy(lambda: _running_log.datastore)

# Blueprint
miles = Blueprint('miles', __name__, url_prefix='/miles')


@miles.route('/')
@login_required
def index():
    # Runs
    now = rltime.now().floor('day')
    start, end = now.span('week')
    this_week, last_week = now.this_week, None
    if now.weekday() <= 2:  # Sunday=0, Monday=1, Tuesday=2
        start = now.replace(weeks=-1).span('week')[0]
        last_week = now.last_week
    runs = models.UserRuns(current_user, start_date=start, end_date=end)

    # Group
#   if current_user.primary_group:
#       group_runs = models.GroupRuns(current_user.primary_group)

    # SJU CC
    johnnie_cc_runs = None
    if current_user.johnnie_cc:
        johnnie_cc_runs = models.JohnnieCCRuns(current_user, 
                start_date=start, end_date=end)

    # Run Entry Form
    run_entry_form = forms.RunEntryForm()
    run_entry_dialog = render_template('miles/run_entry_dialog.html', 
            run_entry_form=run_entry_form)

    return render_template('miles/index.html', 
            now=now, this_week=this_week, last_week=last_week,
            runs=runs, johnnie_cc_runs=johnnie_cc_runs,
            run_entry_dialog=run_entry_dialog)


@miles.route('/run', methods=['POST'])
@login_required
def run():
    form_class = forms.RunEntryForm

    if request.form:
        form = form_class(request.form)
    else:
        raise Exception

    if form.validate_on_submit():
        form.next.data = url_for('.index')
        _datastore.create_or_update_run(current_user, **form.to_dict())
        _datastore.commit()
    else:
        flash_errors(form)

    return render_template('miles/run_entry_dialog.html',
            run_entry_form=form)

