from revcore_micro.ddb.exceptions import InstanceNotFound
from jwcrypto.jwk import JWK
from revcore_micro.flask import exceptions
from revcore_micro.flask.users import User
from revcore_micro.jwt import jwt_decode
import boto3
import jwt
import requests
import json


class BaseVerifier:
    def __init__(self, client_class, region_name='ap-northeast-1'):
        self.client_class = client_class
        self.region_name = region_name

    def verify(self, *args, **kwargs):
        raise NotImplementedError('verify')


class ClientVerifier(BaseVerifier):
    def verify(self, client_id, **kwargs):
        try:
            return self.client_class.get(id=client_id), None
        except InstanceNotFound:
            raise exceptions.PermissionDenied(detail=f'{client_id} not found')


class ClientSecretVerifier(BaseVerifier):
    region_name = 'ap-northeast-1'

    def verify(self, client_secret, **kwargs):
        try:
            client = boto3.client('apigateway', region_name=self.region_name)
            keys = client.get_api_keys(includeValues=True, limit=200)['items']
            key = list(filter(lambda key: key['value'] == client_secret, keys))
            if not key:
                raise Exception('apikey not found')
            key = key[0]
            return self.client_class.get(id=key['name']), None
        except Exception as e:
            raise exceptions.PermissionDenied(detail=str(e))


class JWTVerifier(BaseVerifier):
    token_type = 'access'
    permission_classes = []
    user_instance_class = User

    def get_user_instance(self, user):
        user = self.user_instance_class(client_class=self.client_class, user=user)
        return user

    def check_user_permission(self, user):
        for permission_class in self.permission_classes:
            permission = permission_class(user=user)
            permission.check_user_permission()

    def check_token_type(self, typ):
        if typ != self.token_type:
            detail = f'invalid token type: {typ}'
            raise exceptions.PermissionDenied(detail=detail)

    def decode(self, token):
        decoded = jwt_decode(token, algorithms=['RS256'], verify=True)
        self.check_token_type(decoded['typ'])
        return decoded

    def verify(self, token, **kwargs):
        try:
            user = self.decode(token)
            user = self.get_user_instance(user)
            self.check_user_permission(user)
            client = self.client_class.get(id=user['aud'])
            return client, user
        except Exception as e:
            raise exceptions.PermissionDenied(detail=str(e))


class RefreshVerifier(JWTVerifier):
    token_type = 'refresh'

    def get_user_instance(self, user):
        return user


class CertVerifier(JWTVerifier):
    token_type = 'certificate'

    def verify(self, cert):
        try:
            decoded = self.decode(cert)
            client = self.client_class.get(id=decoded['sub'])
            return client, None
        except Exception as e:
            raise exceptions.PermissionDenied(detail=str(e))
