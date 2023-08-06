import marshmallow as ma
from revcore_micro.flask import exceptions
from functools import wraps


class Serializer(ma.Schema):
    validated_key = 'validated_data'

    def load(self, *args, **kwargs):
        try:
            return super().load(*args, **kwargs)
        except ma.ValidationError as e:
            raise exceptions.ValidationError(e)

    def with_validated_data(self, source='json'):
        def decorated(f):
            from flask import request
            if source == 'json':
                data = request.get_json()
            elif source == 'query':
                data = request.args.to_dict()

            @wraps(f)
            def wrapped(*args, **kwargs):
                result = self.load(data)
                kwargs[self.validated_key] = result
                return f(*args, **kwargs)

            return wrapped
        return decorated
