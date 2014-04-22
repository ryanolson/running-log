# -*- coding: utf-8 -*-
"""
    running_log.core
    ~~~~~~~~~~~~~~~~

    :author: Ryan Olson
    :copyright: (c) 2013 by Ryan Olson
    :license: GPLv3, see LICENSE for more details.
"""

from flask.ext.mail import Mail
mail = Mail()

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.security import Security
security = Security()

from flask.ext.social import Social
social = Social()


class RunningLogError(Exception):
    """Base application error class."""

    def __init__(self, msg):
        self.msg = msg

class RunningLogFormError(Exception):
    """Raise when an error processing a form occurs."""

    def __init__(self, errors=None):
        self.errors = errors


class Service(object):
    """A :class:`BaseService` instance encapsulates common model
    operations in the context of a :class:`Flask` application.
    """
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not the
        expected type.

        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.

        :param kwargs: a dictionary of parameters
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def first(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).first()

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        """Returns an updated instance of the service's model class.

        :param model: the model to update
        :param **kwargs: update parameters
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model)
        return model

    # the remaining functions require specialization

    def save(self, model):
        """Commits the model to the database and returns the model

        :param model: the model to save
        """
        raise NotImplementedError

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        raise NotImplementedError

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param id: the instance id
        """
        raise NotImplementedError

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.

        :param *ids: instance ids
        """
        raise NotImplementedError

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        raise NotImplementedError

    def get_or_404(self, id):
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.

        :param id: the instance id
        """
        raise NotImplementedError

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        raise NotImplementedError

    def delete(self, model):
        """Immediately deletes the specified model instance.

        :param model: the model instance to delete
        """
        raise NotImplementedError


class SQLService(Service):
    """A :class:`Service` instance encapsulates common SQLAlchemy model
    operations in the context of a :class:`Flask` application.
    """
    __model__ = None

    def save(self, model):
        """Commits the model to the database and returns the model

        :param model: the model to save
        """
        self._isinstance(model)
        db.session.add(model)
        db.session.commit()
        return model

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        return self.__model__.query.all()

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.

        :param *ids: instance ids
        """
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.__model__.query.filter_by(**kwargs)

    def get_or_404(self, id):
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.__model__(**self._preprocess_params(kwargs))

    def delete(self, model):
        """Immediately deletes the specified model instance.

        :param model: the model instance to delete
        """
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()


class CouchService(Service):
    """A :class:`Service` instance encapsulates common CouchDB model
    operations in the context of a :class:`Flask` application.
    """
    pass

