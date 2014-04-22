# -*- coding: utf-8 -*-
"""
    tests.api
    ~~~~~~~~~

    api tests package
"""

from running_log.api import create_app

from .. import RunningLogTestCase, settings


class RunningLogApiTestCase(OverholtAppTestCase):

    def _create_app(self):
        return create_app(settings, register_security_blueprint=True)

    def setUp(self):
        super(RunningLogApiTestCase, self).setUp()
        self._login()
