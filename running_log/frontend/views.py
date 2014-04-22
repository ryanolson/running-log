# -*- coding: utf-8 -*-
"""
    views.py
    ~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask import Blueprint, render_template, redirect, current_app, url_for, request
from flask.ext.login import login_required
from flask.ext.security import current_user
from werkzeug.local import LocalProxy
from werkzeug.datastructures import MultiDict

from .. import utils

# Extensions
_social = LocalProxy(lambda: current_app.extensions['social'])
_security = LocalProxy(lambda: current_app.extensions['security'])

# Blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('runs.index'))
    return render_template('frontend/cover.html')

@frontend.route('/privacy')
def privacy():
    return render_template('frontend/privacy.html')

@frontend.route('/terms-of-use')
def terms_of_use():
    return render_template('frontend/terms-of-use.html')

@frontend.route('/profile')
@login_required
def profile():
    profile_url = utils.gravatar_url(current_user.email, size=128)
    return render_template('frontend/profile.html',
        facebook_conn=_social.facebook.get_connection(),
        strava_conn=_social.strava.get_connection(),
        profile_url=profile_url)


@frontend.route('/test/login', methods=['GET', 'POST'])
def test_login():
    form_class = _security.login_form

    if request.json:
        form = form_class(MultiDict(request.json))
    else:
        form = form_class()

    if form.validate_on_submit():
        print "victory"
    else:
        print "fail"

        for field, errors in form.errors.items():
            for error in errors:
                print u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error)
    return "done"
