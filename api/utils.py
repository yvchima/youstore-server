from functools import wraps
from datetime import datetime

from flask import request
from api import db
from api.errors import error_response
from api.models import User


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return error_response(403, message='No authorization.')

        token = auth_header.split(" ")[1]
        payload = User.decode_auth_token(token)

        if not isinstance(payload, dict):
            return error_response(401, message=payload)

        user = User.find_by_id(payload.get('id'))

        if user is None or user.is_active is not True:
            return error_response(401, message='Invalid token.')

        return func(user, *args, **kwargs)
    return wrapper

class ResourceMixin(object):
    created_on = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_on = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    @classmethod
    def find_by_id(cls, id):
        """
        Get a class instance given its id

        :param id: ID
        :type id: int
        :return: Class instance
        """
        return cls.query.get(int(id))

    def save(self):
        """
        Save a model instance.

        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()
