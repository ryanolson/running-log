# -*- coding: utf-8 -*-
"""
    github.py
    ~~~~~~~~~

    Flask-Social extension for Github OAuth Logins

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from stravalib.client import Client

config = {
    'id': 'strava',
    'name': 'Strava',
    'install': 'pip install stravalib',
    'module': 'app.strava',
    'base_url': 'https://www.strava.com/api/v3',
    'request_token_url': None,
    'authorize_url': 'https://www.strava.com/oauth/authorize',
    'request_token_params': {
        'response_type': 'code',
    },
    'access_token_url': 'https://www.strava.com/oauth/token',
    'access_token_method': 'POST',
}


def get_api(connection, **kwargs):
    return Client(access_token=getattr(connection, 'access_token'))


def get_provider_user_id(response, **kwargs):
    if response:
        client = Client(access_token=response['access_token'])
        user = client.get_athlete()
        return str(user.id)
    return None


def get_connection_values(response, **kwargs):
    if not response:
        return None

    access_token = response['access_token']
    client = Client(access_token=access_token)
    user = client.get_athlete()

    full_name = "{0} {1}".format(user.firstname, user.lastname)

    return dict(
        provider_id=config['id'],
        provider_user_id=str(user.id),
        access_token=access_token,
        secret=None,
        display_name=full_name,
        full_name=full_name,
        profile_url="http://www.strava.com/athletes/{0}".format(user.id),
        image_url=user.profile,
    )
