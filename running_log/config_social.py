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
        'consumer_key': '272895716208605',
        'consumer_secret': 'd287eaf678e545777e91696921cf0e96',
        'request_token_params': {
            'scope': 'email, user_education_history',
        },
    },
    'github': { 
        'consumer_key': 'c74fbb9ca61717d0e431',
        'consumer_secret': '03ecb6034c4c8b741c66112ffb0c535af5a66591',
        'module': 'running_log.github',
    },
    'strava': { 
        'consumer_key': '1207',
        'consumer_secret': '78f4310db291ba03a9f8900a1332c86314434533',
        'module': 'running_log.strava',
    },
}

