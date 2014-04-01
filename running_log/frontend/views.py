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
from ..utils import this_week, Runs
from ..models.sqlalchemy import User, Run

# Extensions
_social = LocalProxy(lambda: current_app.extensions['social'])

# Blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    if current_user:
        return redirect(url_for('.miles'))
    return render_template('frontend/index.html')

@frontend.route('/miles')
@login_required
def miles():
    now = arrow.now('US/Central').floor('day')
    runs = Runs(current_user)
    run_entry_form = RunEntryForm()
    run_entry_dialog = render_template('frontend/run_entry_dialog.html', 
            run_entry_form=run_entry_form)
    return render_template('frontend/miles.html', this_week=this_week(),
            run_entry_dialog=run_entry_dialog, now=now, runs=runs)

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
        profile_url=profile_url
    )

