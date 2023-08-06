from functools import wraps
from flask import request
from revcore_micro.utils import DecimalEncoder
from revcore_micro.flask.exceptions import APIException, exception_handler

def with_page(model):
    def decorated(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = {model.partition_key: request.args.get(model.partition_key)}
            if model.sort_key:
                key[model.sort_key] = request.args.get(model.sort_key)

            kwargs['last_key'] = key
            return f(*args, **kwargs)

        return wrapped

    return decorated


def set_default(app):
    app.json_encoder = DecimalEncoder
    app.register_error_handler(APIException, exception_handler)
