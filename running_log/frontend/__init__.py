# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by What's Brewing LLC
    :license: What's Brewing LLC Proprietary, see LICENSE for more details.
"""
from functools import wraps

from flask import render_template
from flask.ext.security import login_required

from .. import factory
#from . import assets
from . import extensions


def create_app(settings_override=None):
    """Returns the RunningLog application instance"""
    app = factory.create_app(__name__, __path__, settings_override)

    # Init assets
    # assets.init_app(app)

    # Flask-Babel
    extensions.babel.init_app(app)

    # Flask-Bootstrap
    extensions.bootstrap.init_app(app)

    # Register custom error handlers
    if not app.debug:
        for e in [500, 404]:
            app.errorhandler(e)(handle_error)

    return app


def handle_error(e):
    return render_template('errors/%s.html' % e.code), e.code


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator

