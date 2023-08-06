from flask import request, jsonify
from functools import wraps
from revcore_micro.flask.verifiers import ClientVerifier, JWTVerifier, ClientSecretVerifier
from flask import current_app


class Authorizer:
    region_name = 'ap-northeast-1'
    client_class = None
    client_verifier_class = ClientVerifier
    jwt_verifier_class = JWTVerifier
    client_secret_verifier_class = ClientSecretVerifier

    @classmethod
    def authorize(cls, *config, **config_args):
        def decorated(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                verifier_class, params = cls.get_verifier_info(*config, **config_args)
                verifier = verifier_class(client_class=cls.client_class, region_name=cls.region_name)
                client, user = verifier.verify(**params)

                kwargs['client'] = client
                kwargs['user'] = user
                return f(*args, **kwargs)

            return wrapped

        return decorated

    @classmethod
    def get_verifier_info(cls,
                          with_client=False,
                          with_jwt=False,
                          with_client_secret=False,
                          with_cert=True,
                          force_client=True,
                          force_jwt=True,
                          force_secret=True,
                          force_cert=True):

        client_id = request.args.get('client_id')
        token = request.args.get('token')
        client_secret = request.headers.get('x-api-key', None)
        cert = request.args.get('certificate')

        if (with_client and force_client) or (with_client and client_id):
            return cls.client_verifier_class, {'client_id': client_id}
        elif (with_jwt and force_jwt) or (with_jwt and token):
            return cls.jwt_verifier_class, {'token': token}
        elif (with_client_secret and force_secret) or (with_client_secret and client_secret):
            request.is_server = True
            return cls.client_secret_verifier_class, {'client_secret': client_secret}
        elif(with_cert and force_cert) or (with_cert and cert):
            request.is_service = True
            return cls.cert_verifier_class, {'cert': cert}
