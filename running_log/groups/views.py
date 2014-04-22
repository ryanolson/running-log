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

from .. import forms
from .. import rltime
from .. import utils
from ..miles import models as miles_models

_running_log = LocalProxy(lambda: current_app.extensions['running_log'])
_datastore = LocalProxy(lambda: _running_log.datastore)

# Blueprint
groups = Blueprint('groups', __name__, url_prefix='/groups')

@groups.route('/')
@login_required
def index():
    """Returns a list of groups to which the user belongs."""
    return render_template('groups/index.html')

@groups.route('/details/<group_id>')
@login_required
def details(group_id):
    """Mileage chart for the group."""
    group = _datastore.find_group(id=group_id)
    group_runs = _datastore.group_runs(group)
    return render_template('groups/details.html',
            group=group, group_run=group_runs)

@groups.route('/list/<page>')
@groups.route('/list')
@login_required
def list(page=None):
    """List of all groups."""
    page = int(page) if page else 1
    groups = _datastore.public_groups(page, per_page=12)
    return render_template('groups/list.html',
            groups=groups)


@groups.route('/johnnie-cc')
@login_required
def johnnie_cc():
    today = rltime.now()
    group_runs = miles_models.JohnnieCCRuns(current_user, all_years=True)
    return render_template('groups/johnnie_cc.html', group_runs=group_runs,
            today=today, this_week=today.this_week)
