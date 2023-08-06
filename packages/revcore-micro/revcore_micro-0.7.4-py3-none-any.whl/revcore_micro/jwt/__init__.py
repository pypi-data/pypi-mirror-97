import boto3
import random
from collections.abc import Iterable, Mapping
from datetime import datetime, timedelta
from jwt.algorithms import Algorithm, RSAAlgorithm
from jwt.api_jwt import PyJWT
from jwt.api_jws import PyJWS
from jwt.exceptions import (
    DecodeError,
    InvalidAlgorithmError,
    InvalidSignatureError,
    InvalidTokenError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAudienceError,
    InvalidIssuedAtError,
    InvalidIssuerError,
    MissingRequiredClaimError,
)
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
    load_ssh_public_key,
)

from calendar import timegm
import requests
import json
from jwcrypto.jwk import JWK


class KMSAlgorithm(RSAAlgorithm):
    region = 'ap-northeast-1'

    def __init__(self, *args, **kwargs):
        self.hash_alg = RSAAlgorithm.SHA256

    def get_client(self):
        client = boto3.client('kms', self.region)
        return client

    def prepare_key(self, key):
        return key

    def sign(self, msg, key):
        client = self.get_client()
        resp = client.sign(KeyId=key, Message=msg, SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256')
        return resp['Signature']

    def verify(self, msg, key, sig):
        real_key = load_pem_public_key(key)
        return super().verify(msg, real_key, sig)


class JWS(PyJWS):
    def __init__(self, options=None):
        super().__init__(options)
        self._algorithms = {'RS256': KMSAlgorithm()}

    def decode_complete(
        self,
        jwt,
        key="",
        algorithms=None,
        options=None,
        **kwargs,
    ):
        if options is None:
            options = {}
        merged_options = {**self.options, **options}
        verify_signature = merged_options["verify_signature"]

        if verify_signature and not algorithms:
            raise DecodeError(
                'It is required that you pass in a value for the "algorithms" argument when calling decode().'
            )

        payload, signing_input, header, signature = self._load(jwt)

        json_payload = json.loads(payload.decode())
        host, version = json_payload['iss'].split('/')
        kid = header['kid']
        env = host.split('.')[0][-4:]
        if env in ['-stg', '-dev']:
            host = 'https://auth-stg.revtel-api.com'
        else:
            host = 'https://auth.revtel-api.com'

        if version == 'v3':
            url = f'{host}/{version}/certs'
            resp = requests.get(url).json()['keys']
            key = [key for key in resp if key['kid'] == kid][0]
        else:
            resp = requests.get('https://keys.revtel-api.com/pub.json').json()
            key = [key for key in resp if key['kid'] == kid][0]
        key = JWK.from_json(json.dumps(key))
        key = key.export_to_pem()

        if verify_signature:
            self._verify_signature(signing_input, header, signature, key, algorithms)

        return {
            "payload": payload,
            "header": header,
            "signature": signature,
        }


_jws = JWS()
encode = _jws.encode
decode = _jws.decode_complete


class JWT(PyJWT):
    def encode(
        self,
        payload,
        key,
        algorithm='RSA256',
        headers=None,
        json_encoder=None,
    ):
        # Check that we get a mapping
        if not isinstance(payload, Mapping):
            raise TypeError(
                "Expecting a mapping object, as JWT only supports "
                "JSON objects as payloads."
            )

        # Payload
        payload = payload.copy()
        for time_claim in ["exp", "iat", "nbf"]:
            # Convert datetime to a intDate value in known time-format claims
            if isinstance(payload.get(time_claim), datetime):
                payload[time_claim] = timegm(payload[time_claim].utctimetuple())

        json_payload = json.dumps(
            payload, separators=(",", ":"), cls=json_encoder
        ).encode("utf-8")

        return encode(json_payload, key, algorithm, headers, json_encoder)

    def decode_complete(
        self,
        jwt,
        key="",
        algorithms=None,
        options=None,
        **kwargs,
    ):
        if options is None:
            options = {"verify_signature": True}
        else:
            options.setdefault("verify_signature", True)

        if options["verify_signature"] and not algorithms:
            raise DecodError(
                'It is required that you pass in a value for the "algorithms" argument when calling decode().'
            )

        decoded = decode(
            jwt,
            key=key,
            algorithms=algorithms,
            options=options,
            **kwargs,
        )

        try:
            payload = json.loads(decoded["payload"])
        except ValueError as e:
            raise DecodeError("Invalid payload string: %s" % e)
        if not isinstance(payload, dict):
            raise DecodeError("Invalid payload string: must be a json object")

        if options["verify_signature"]:
            merged_options = {**self.options, **options}
            self._validate_claims(payload, merged_options, **kwargs)

        decoded["payload"] = payload
        return decoded

    def _validate_aud(self, payload, audience):
        if audience is None:
            return
        if audience is None and "aud" not in payload:
            return

        if audience is not None and "aud" not in payload:
            # Application specified an audience, but it could not be
            # verified since the token does not contain a claim.
            raise MissingRequiredClaimError("aud")

        audience_claims = payload["aud"]

        if isinstance(audience_claims, str):
            audience_claims = [audience_claims]
        if not isinstance(audience_claims, list):
            raise InvalidAudienceError("Invalid claim format in token")
        if any(not isinstance(c, str) for c in audience_claims):
            raise InvalidAudienceError("Invalid claim format in token")

        if isinstance(audience, str):
            audience = [audience]

        if not any(aud in audience_claims for aud in audience):
            raise InvalidAudienceError("Invalid audience")


_jwt = JWT()
jwt_encode = _jwt.encode
jwt_decode = _jwt.decode


class JWTEncoder:
    default_payload_classes = None
    key_class = None

    def __init__(self, client):
        self.client = client

    def get_payload_classes(self):
        return self.default_payload_classes.__members__.items()

    def get_private_key(self):
        keys = self.key_class.query(alg='RSA256', status='enabled', index_name='alg-status-index')
        key = random.choice(keys)
        return key['id']

    def build_payload(self, user):
        payload_classes = self.get_payload_classes()
        payload = {}
        for name, member in payload_classes:
            builder = member.value(client=self.client)
            payload[name] = builder.build_payload(user)

        return payload

    def encode(self, user):
        key = self.get_private_key()
        data = self.build_payload(user)
        headers = {'kid': key}
        encoded = jwt_encode(data, key=key, algorithm='RS256', headers=headers)
        return encoded
