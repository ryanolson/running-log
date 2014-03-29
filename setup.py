# -*- coding: utf-8 -*-
"""
    setup.py
    ~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""

from setuptools import setup, find_packages

setup(
    name='running_log',
    version='0.0.1',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    setup_requires=[
    ],
    install_requires=[
        'clapp',
        'Flask-Security',
        'flask-mongoengine',
    ],
    scripts=[
        'scripts/running_logctl',
    ],
    dependency_links = [
    ]
)
