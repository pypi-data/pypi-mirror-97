from datetime import datetime
from datetime import timedelta
from functools import wraps

import jwt

from flask import current_app
from flask import g
from flask import request

from handyhttp.exceptions import HTTPForbidden
from handyhttp.exceptions import HTTPDenied


class Roles:
    ADMIN = 'Admin'
    USER = 'General'
    SUPER = 'SuperUser'


def admin_only(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_token = confirm_token()
        if not auth_token:
            raise HTTPForbidden()
        if type(auth_token) == str:
            raise HTTPDenied()
        user_id = auth_token.get('user')
        # user = UserDAO().get(user_id)
        # if user.permission and Roles.ADMIN.lower() in [i.role.lower() for i in user.permission]:
        #     return func(*args, **kwargs)
        return HTTPDenied().pack()
    return decorated


def encode_auth_token(user_id=None, expiry=36006, additional=None, sk=None, algo='HS256'):
    if not expiry:
        expiry = current_app.config.get('JWT_TOKEN_EXPIRY', expiry)
    if not user_id:
        user_id = g.user

    secret_key = sk or current_app.config.get('SECRET_KEY', None)
    if not secret_key:
        raise ValueError('No SECRET_KEY found in config or passed to decorators.')

    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=expiry),
            'iat': datetime.utcnow(),
            'sub': '{}'.format(user_id)
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm=algo
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token, secret=None):
    if not secret:
        secret = current_app.config.get('SECRET_KEY')
    try:
        payload = jwt.decode(auth_token, secret, algorithms='HS256')
        return {
            'user': payload['sub'],
            'access': True
        }
    except Exception as exc:
        pass
    except jwt.ExpiredSignatureError:
        return 'Auth token expired. Please log in again'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again'


def confirm_token(token=None):
    try:
        if not token:
            token = request.headers.environ.get('HTTP_API_AUTHORIZATION')
        decoded = decode_auth_token(token)
    except Exception as error:
        return None
    return decoded


def check_request_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_token = confirm_token()
        if not auth_token:
            return HTTPForbidden().pack()
        if type(auth_token) == str:
            return HTTPDenied().pack()

        g.user = auth_token.get('user')

        if request.method == 'GET':
            return func(*args, **kwargs)
        kwargs['user'] = g.user
        return func(*args, **kwargs)

    return decorated
