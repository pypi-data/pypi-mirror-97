from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import DoesNotExist

from .dao import AbstractDAO


class UserModel(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = 'wellness'
        region = 'eu-west-1'
    email = UnicodeAttribute(hash_key=True)
    fullname = UnicodeAttribute()
    password = UnicodeAttribute()


class DynamoDAO(AbstractDAO):
    def __init__(self):
        super().__init__()
        UserModel.create_table(write_capacity_units=1, read_capacity_units=1)

    def auth(self, payload, **kwargs):
        username, password = payload.get('username'), payload.get('password')

        try:
            user = UserModel.get(username)
            return user.email, user.password, user
        except DoesNotExist:
            raise ValueError()

    def get(self, *args, **kwargs):
        pass

    def one(self, resource, *args, **kwargs):
        pass

    def validate(self, lookup=None, field=None):
        pass

    def sanitize_payload(self):
        pass

    def post(self, payload):
        pass

    def delete(self, resource):
        pass



