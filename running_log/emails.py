# -*- coding: utf-8 -*-                                                                                                     
"""
    emails.py
    ~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask.ext.mail import Message

from . import extensions
from . import decorators

@decorators.async
def send_async_email(message)
    extensions.mail.send(msg)

@extensions.security.send_mail_task
def async_security_email(msg):
    send_async_email(msg)

def send_message(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)
