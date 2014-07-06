# -*- coding: utf-8 -*-
"""
    wsgi.py
    ~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

#from running_log import api
from running_log import frontend

application = DispatcherMiddleware(frontend.create_app(), {
#    '/api': api.create_app()
})

if __name__ == "__main__":
    run_simple('0.0.0.0', 12346, application, use_reloader=True, use_debugger=True)
