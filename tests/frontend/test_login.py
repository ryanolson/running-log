# -*- coding: utf-8 -*-
"""
    tests.api.user_tests
    ~~~~~~~~~~~~~~~~~~~~

    api user tests module
"""

from . import RunningLogFrontendTestCase

class TestUser(RunningLogFrontendTestCase):

    def test_user(self):
        assert self.user.password == 'password'

class TestLogin(RunningLogFrontendTestCase):

    def test_authenticated_dashboard_access(self):
        r = self.get('/')
        self.assertOk(r)
        self.assertNotIn('Register', r.data)

    def test_unauthenticated_dashboard_access(self):
        self.get('/logout')
        r = self.get('/')
        self.assertOk(r)
        self.assertIn('Register', r.data)
