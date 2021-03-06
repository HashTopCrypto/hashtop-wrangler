from functools import wraps
from flask import request

from app.main.service.auth_helper import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        # get logged in user returns object, status code
        # if there is no token, we know that a user isn't logged in
        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated


def api_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.validate_api_token(request)

        # if we dont get 200 from the auth helper, the token wasn't valid
        if status != 200:
            return data, status

        return f(*args, **kwargs)

    return decorated
