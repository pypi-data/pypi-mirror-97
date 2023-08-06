from flask import current_app
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from handyhttp.exceptions import HTTPConflict
from handyhttp.exceptions import HTTPNotAcceptable


PASSWORD_MIN = 4
USERNAME_MIN = 4


class AbstractDAO:

    def auth(self, payload, **kwargs):
        raise NotImplementedError()

    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def one(self, resource, *args, **kwargs):
        raise NotImplementedError()

    def validate(self, lookup=None, field=None):
        raise NotImplementedError()

    def sanitize_payload(self):
        raise NotImplementedError()

    def post(self, payload):
        raise NotImplementedError()

    def delete(self, resource):
        raise NotImplementedError()
