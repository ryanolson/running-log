# -*- coding: utf-8 -*-
"""
    views.py
    ~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import arrow
from clapp.forms import flash_errors
from flask import Blueprint, render_template, redirect, session, current_app
from flask import request, url_for, jsonify
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.security import current_user
from werkzeug.local import LocalProxy

from ..forms import RunEntryForm
from ..utils import Runs, last_week, create_or_update_run_from_form
from .. import utils
from .. import rl_arrow
from ..models.sqlalchemy import User, Run

# Extensions
_social = LocalProxy(lambda: current_app.extensions['social'])

# Blueprint
miles = Blueprint('miles', __name__, url_prefix='/miles')

@miles.route('/')
@login_required
def index():
    now = arrow.now('US/Central').floor('day')
    current_week = utils.this_week()
    runs = Runs(current_user)
    runs_last_week = None
    if now.weekday() <= 1 or now.weekday() == 6: # only show last week on Sunday, Monday and Tues
        runs_last_week = Runs(current_user, dates=utils.last_week())
    run_entry_form = RunEntryForm()
    run_entry_dialog = render_template('miles/run_entry_dialog.html', 
            run_entry_form=run_entry_form)
    group_runs = None
    if current_user.johnnie_cc:
        group_users = utils.runs_for_overlapping_johnnies(current_user)
        group_runs = [Runs(user, dates=current_week) for user in group_users]
        group_runs_lw = [Runs(user, dates=utils.last_week()) for user in group_users]
    return render_template('miles/index.html', this_week=utils.this_week(),
            run_entry_dialog=run_entry_dialog, now=now, runs=runs,
            runs_last_week=runs_last_week, group_runs=group_runs)

# -- @miles.route('/')
# -- @login_required
# -- def index():
# --     # Runs
# --     today = rl_arrow.now().sod
# --     if today.weekday() <= 2:  # Sunday=0, Monday=1, Tuesday=2
# --         runs = UserRuns(current_user, start_date=today.replace(weeks=-1).sow,
# --                 end_date=today.eow)
# --     else:
# --         runs = UserRuns(current_user)
# -- 
# --     # Run Entry Form
# --     run_entry_form = RunEntryForm()
# --     run_entry_dialog = render_template('miles/run_entry_dialog.html', 
# --             run_entry_form=run_entry_form)
# -- 
# --     # Group
# --     # determine default group
# --     # load Users and UserRuns for 
# --     group_runs = None
# --     if current_user.johnnie_cc:
# --         group_users = utils.runs_for_overlapping_johnnies(current_user)
# --         group_runs = [Runs(user, dates=current_week) for user in group_users]
# --         group_runs_lw = [Runs(user, dates=utils.last_week()) for user in group_users]
# --     return render_template('miles/index.html', this_week=utils.this_week(),
# --             run_entry_dialog=run_entry_dialog, now=now, runs=runs,
# --             runs_last_week=runs_last_week, group_runs=group_runs)
# -- 

@miles.route('/run', methods=['POST'])
@login_required
def run():
    form_class = RunEntryForm

    if request.form:
        form = form_class(request.form)
    else:
        raise Exception

    if form.validate_on_submit():
        form.next.data = url_for('.index')
        create_or_update_run_from_form(current_user, form)
    else:
        flash_errors(form)

    return render_template('miles/run_entry_dialog.html',
            run_entry_form=form)

