from flask import Flask
from flask import request
from flask import Blueprint
from flask import current_app

from handyhttp.exceptions import HTTPConflict
from handyhttp.exceptions import HTTPForbidden
from handyhttp.exceptions import HTTPException
from handyhttp.exceptions import HTTPDenied
from handyhttp.responses import HTTPSuccess
from werkzeug.security import check_password_hash

from .decorators import check_request_token
from .decorators import encode_auth_token


class AuthBlueprint(Blueprint):

    def __init__(self, dao, **kwargs):
        super().__init__(__name__, 'auth-blueprint-instance')
        self.dao = dao
        self.register_endpoints()
        self.response = self.response
        self.errors = False
        for key, value in kwargs.items():
            setattr(self, key, value)

        if self.errors:
            @self.app_errorhandler(Exception)
            def error_handler(exc):
                if isinstance(exc, HTTPException):
                    return exc.pack()
                raise exc

        self.register_endpoints()

    def setup(self, app: Flask):
        app.register_blueprint(self)

    def check_user_password(self, password, stored):
        return check_password_hash(password, stored)

    def response(self, data):
        if isinstance(data, tuple):
            return data
        if not isinstance(data, (dict, list, str)):
            raise ValueError('Cannot handle non-serialized objects for JSON response')
        return HTTPSuccess(data)

    def register_endpoints(self):
        if not self.dao:
            raise RuntimeError('Auth module requires a DAO service')
        self.add_url_rule('/authenticate', 'authenticate', self.authenticate, methods=['POST'])
        self.add_url_rule('/authenticate/', 'authenticate_', self.authenticate, methods=['POST'])
        self.add_url_rule('/', 'create', self.create, methods=['POST'])
        self.add_url_rule('', 'create_', self.create, methods=['POST'])
        self.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.add_url_rule('/self', 'self', self.get, methods=['GET'])
        self.add_url_rule('/self/', 'self_', self.get, methods=['GET'])
        self.add_url_rule('/confirm', 'confirm', self.confirm, methods=['GET'])

        self.add_url_rule('/<key>', 'one', self.one, methods=['GET'])
        self.add_url_rule('/<key>/', 'one_', self.one, methods=['GET'])

        self.add_url_rule('/<key>/<path:resource>', 'one', self.one, methods=['GET'])
        self.add_url_rule('/<key>/<path:resource>/', 'one_', self.one, methods=['GET'])

    @check_request_token
    def index(self):
        user = self.dao.get()
        return self.response(user)

    @check_request_token
    def one(self, key):
        user = self.dao.one(key)
        return self.response(user)

    @check_request_token
    def get(self):
        user = self.dao.get()
        self.response(user)

    def serialize(self, model):
        raise NotImplementedError()

    def create(self):
        payload = request.json
        try:
            user = self.dao.post(payload)
        except HTTPConflict as exc:
            raise exc
        return self.response(user)

    @check_request_token
    def confirm(self):
        return self.response(HTTPSuccess())

    def authenticate(self):
        payload = request.json
        conf = current_app.config.get('ATOMIC')

        if conf.get('TESTING', False):
            if conf.get('PASSWORD') == payload.get('password') and conf.get('USERNAME') == payload.get('username'):
                username = conf.get('USERNAME')
                auth_token = encode_auth_token(str(username))
                return HTTPSuccess(token=auth_token)

        try:
            username, password, model = self.dao.auth(payload)
        except ValueError:
            raise HTTPDenied()

        if not username:
            raise HTTPDenied()
        verified = self.check_user_password(password, payload.get('password'))
        if not verified:
            raise HTTPForbidden()

        auth_token = encode_auth_token(str(username))
        return HTTPSuccess(
            token=auth_token,
            user=model
        )
