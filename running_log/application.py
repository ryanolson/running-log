# -*- coding: utf-8 -*-
"""
    application.py
    ~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""
from clapp import Clapp
from flask.ext.security import UserMixin, RoleMixin
from flask.ext.security import SQLAlchemyUserDatastore
from flask.ext.social import SQLAlchemyConnectionDatastore

from . import config
from .extensions import db, security, social
from .frontend.views import frontend
from .miles.views import miles

BLUEPRINTS = (
    frontend,
    miles,
)

DOCUMENTS = (
)

class _RunningLogState(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)
    

class RunningLog(Clapp):
    
    def configure_extensions(self):
        super(RunningLog, self).configure_extensions()

        # Flask-SQLAlchemy
        db.init_app(self.app)

        # Flask-Security
        from .models.sqlalchemy import Role, User
        from .forms import ExtendedRegisterForm
        self.user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(self.app, self.user_datastore,
                register_form=ExtendedRegisterForm)

        # Flask-Social
        from models.sqlalchemy import Connection
        self.connections_datastore = SQLAlchemyConnectionDatastore(db, Connection)
        social.init_app(self.app, self.connections_datastore)
 
        # Running Log
        from .datastore import SQLAlchemyRunningLogDatastore
        from .models.sqlalchemy import Run, Group
        datastore = SQLAlchemyRunningLogDatastore(db, User, Run, Group)
        self.app.extensions['running_log'] = _RunningLogState(**{
            "datastore": datastore,
        })
     
        # Flask-MongoEngine
        # db.init_app(self.app)

        # Flask-Security
        # from models.mongo import Role, User
        # self.user_datastore = MongoEngineUserDatastore(db, User, Role)
        # security.init_app(self.app, self.user_datastore)

        # Flask-Social
        # from models.mongo import Connection
        # self.connections_datastore = MongoEngineConnectionDatastore(db, Connection)
        # social.init_app(self.app, self.connections_datastore)

def create_app(config=config.Config, blueprints=BLUEPRINTS, documents=DOCUMENTS, **kwargs):
    clapp = RunningLog(__name__, config, blueprints, documents, **kwargs)
    app = clapp.app
    
    @app.before_first_request
    def create_user():
        try:
            db.create_all()
        except Exception, e:
            app.logger.error(str(e))
        #clapp.user_datastore.create_user(email='rmolson@gmail.com', password='password')
        db.session.commit()

    return app

