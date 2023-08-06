from datetime import datetime, timedelta
from uuid import uuid4
from enum import Enum


class BaseBuilder:
    def __init__(self, client):
        self.client = client

    def build_payload(self, user):
        raise NotImplementedError


class AccessTypBuilder(BaseBuilder):
    token_type = 'access'

    def build_payload(self, user):
        return self.token_type


class RefreshTypBuilder(AccessTypBuilder):
    token_type = 'refresh'


class AudBuilder(BaseBuilder):
    def build_payload(self, user):
        return self.client['id']


class IatBuilder(BaseBuilder):
    def build_payload(self, user):
        now = datetime.utcnow()
        return int(now.timestamp())


class JtiBuilder(BaseBuilder):
    def build_payload(self, user):
        return uuid4().__str__()


class SubBuilder(BaseBuilder):
    def build_payload(self, user):
        return user['id']


class GrpBuilder(BaseBuilder):
    def build_payload(self, user):
        groups = user.get('groups', [])
        return ':'.join(groups)


class AccessExpBuilder(BaseBuilder):
    exp_field = 'default_access_exp'
    duration_unit = 'minutes'
    default_exp = 120

    def build_payload(self, user):
        exp = self.client.get(self.exp_field, self.default_exp)
        now = datetime.utcnow()
        kwargs = {self.duration_unit: exp}
        duration = timedelta(**kwargs)
        real_exp = int((now + duration).timestamp())
        return real_exp


class RefreshExpBuilder(AccessExpBuilder):
    exp_field = 'default_refresh_exp'
    duration_unit = 'days'
    default_exp = 7
