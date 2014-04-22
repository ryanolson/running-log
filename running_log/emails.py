# -*- coding: utf-8 -*-                                                                                                     
"""
    running_log.emails
    ~~~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from flask.ext.mail import Message

from .core import mail, security
from .decorators import async

@async
def send_async_email(message)
    mail.send(msg)

@security.send_mail_task
def async_security_email(msg):
    send_async_email(msg)

def send_message(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)
