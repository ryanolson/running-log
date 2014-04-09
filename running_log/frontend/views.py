# -*- coding: utf-8 -*-
"""
    views.py
    ~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask import Blueprint, render_template, redirect, current_app, url_for
from flask.ext.login import login_required
from flask.ext.security import current_user
from werkzeug.local import LocalProxy

from .. import utils

# Extensions
_social = LocalProxy(lambda: current_app.extensions['social'])

# Blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('miles.index'))
    return render_template('frontend/cover.html')

@frontend.route('/profile')
@login_required
def profile():
    profile_url = None
#   for conn in current_user.connections:
#       if conn.image_url:
#           profile_url = conn.image_url
#           break
    if profile_url is None:
        profile_url = utils.gravatar_url(current_user.email, size=128)
    return render_template('frontend/profile.html',
        facebook_conn=_social.facebook.get_connection(),
        github_conn=_social.github.get_connection(),
        strava_conn=_social.strava.get_connection(),
        profile_url=profile_url
    )

@frontend.route('/privacy')
def privacy():
    return render_template('frontend/privacy.html')

@frontend.route('/terms-of-use')
def terms_of_use():
    return render_template('frontend/terms-of-use.html')
