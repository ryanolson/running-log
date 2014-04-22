# -*- coding: utf-8 -*-
"""
    github.py
    ~~~~~~~~~

    Flask-Social extension for Github OAuth Logins

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
import github3

config = {
    'id': 'github',
    'name': 'GitHub',
    'install': 'pip install github3.py',
    'module': 'app.github',
    'base_url': 'https://api.github.com/',
    'request_token_url': None,
    'access_token_url': 'https://github.com/login/oauth/access_token',
    'authorize_url': 'https://github.com/login/oauth/authorize',
    'request_token_params': {
        'scope': 'user'
    }
}


def get_api(connection, **kwargs):
    return github3.login(token=getattr(connection, 'access_token'))


def get_provider_user_id(response, **kwargs):
    if response:
        gh = github3.login(token=response['access_token'])
        return str(gh.user().to_json()['id'])
    return None


def get_connection_values(response, **kwargs):
    if not response:
        return None

    access_token = response['access_token']
    gh = github3.login(token=access_token)
    user = gh.user().to_json()

    from pprint import pprint
    pprint(user)

    return dict(
        provider_id=config['id'],
        provider_user_id=str(user['id']),
        access_token=access_token,
        secret=None,
        display_name=user['login'],
        full_name=user['name'],
        profile_url=user['html_url'],
        image_url=user['avatar_url']
    )
