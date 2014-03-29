# -*- coding: utf-8 -*-
"""
    config_social.py
    ~~~~~~~~~~~~~~~~

    API and Secrets for OAuth providers

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""

CONNECTIONS = {
    'facebook': {
        'consumer_key': '235050360020182',
        'consumer_secret': '9f4b2c6acbf485bfd9942dd7c8b8320b',
        'request_token_params': {
            'scope': 'email,publish_stream',
        },
    },
    'github': { 
        'consumer_key': 'c74fbb9ca61717d0e431',
        'consumer_secret': '03ecb6034c4c8b741c66112ffb0c535af5a66591',
        'module': 'running_log.github',
    },
}

