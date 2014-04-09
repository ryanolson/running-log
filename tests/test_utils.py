# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import pytest
import datetime
from running_log import utils

class TestUtils:

    def test_gravatar_url(self):
        url = utils.gravatar_url('rmolson@gmail.com')
        assert 'http://www.gravatar.com/avatar/710874b630f0c67517df9d070f1ec0ff' in url
