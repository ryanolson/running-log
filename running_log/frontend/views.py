# -*- coding: utf-8 -*-
"""
    views.py
    ~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask import Blueprint, render_template, redirect, session, current_app
from flask import request, url_for
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.security import current_user
from werkzeug.local import LocalProxy

from ..forms import RunEntryForm

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
    run_entry_form = RunEntryForm()
    return render_template('frontend/miles.html', run_entry_form=run_entry_form)

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

#
#@frontend.route('/login', methods=['GET', 'POST'])
#def login():
#    form = forms.LoginForm()
#    if form.validate_on_submit():
#        user = User.authenticate(form.username_or_email.data, form.password.data)
#        if user:
#            login_user(user)
#            return redirect(request.args.get('next') or '/')
#    return render_template('clapp/signin.html', form=form, 
#                           login_view=extensions.login_manager.login_view)
#
#
#@frontend.route('/logout', methods=['GET', 'POST'])
#@login_required
#def logout():
#    logout_user()
#    for key in ('identity.name', 'identity.auth_type'):
#        session.pop(key, None)
#    return redirect(request.args.get('next') or '/')
