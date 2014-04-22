# -*- coding: utf-8 -*-
"""
    tests.frontend
    ~~~~~~~~~~~~~~

    frontend tests package
"""

from running_log.frontend import create_app

from .. import RunningLogAppTestCase, settings


class RunningLogFrontendTestCase(RunningLogAppTestCase):

    def _create_app(self):
        return create_app(settings)

    def setUp(self):
        super(RunningLogFrontendTestCase, self).setUp()
        self._login()
