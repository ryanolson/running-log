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
from ..utils import Runs, this_week, last_week, create_or_update_run_from_form
from .. import utils
from ..models.sqlalchemy import User, Run

# Extensions
_social = LocalProxy(lambda: current_app.extensions['social'])

# Blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('.miles'))
    return render_template('frontend/cover.html')

@frontend.route('/miles')
@login_required
def miles():
    now = arrow.now('US/Central').floor('day')
    current_week = utils.this_week()
    runs = Runs(current_user)
    runs_last_week = None
    if now.weekday() <= 1: # only show last week on Sunday and Monday
        runs_last_week = Runs(current_user, dates=last_week())
    run_entry_form = RunEntryForm()
    run_entry_dialog = render_template('frontend/run_entry_dialog.html', 
            run_entry_form=run_entry_form)
    group_runs = None
    if current_user.johnnie_cc:
        group_users = utils.runs_for_overlapping_johnnies(current_user)
        group_runs = [Runs(user, dates=current_week) for user in group_users]
    return render_template('frontend/miles.html', this_week=this_week(),
            run_entry_dialog=run_entry_dialog, now=now, runs=runs,
            runs_last_week=runs_last_week, group_runs=group_runs)

@frontend.route('/run', methods=['POST'])
@login_required
def run():
    form_class = RunEntryForm

    if request.form:
        form = form_class(request.form)
    else:
        raise Exception

    if form.validate_on_submit():
        form.next.data = url_for('.miles')
        create_or_update_run_from_form(current_user, form)
    else:
        flash_errors(form)

    return render_template('frontend/run_entry_dialog.html',
            run_entry_form=form)

@frontend.route('/profile')
@login_required
def profile():
    profile_url = None
    for conn in current_user.connections:
        if conn.image_url:
            profile_url = conn.image_url
            break
    
    return render_template('frontend/profile.html',
        facebook_conn=_social.facebook.get_connection(),
        github_conn=_social.github.get_connection(),
        strava_conn=_social.strava.get_connection(),
        profile_url=profile_url
    )

