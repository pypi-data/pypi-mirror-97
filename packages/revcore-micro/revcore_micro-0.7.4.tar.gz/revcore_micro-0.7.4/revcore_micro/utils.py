from decimal import Decimal, ROUND_HALF_UP
import decimal
import json
from boto3.dynamodb.types import Binary


def round(f):
    return Decimal(f'{f}').quantize(0, ROUND_HALF_UP).__int__()


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        if isinstance(o, decimal.Decimal):
            value = float(o)
            if value.is_integer():
                return int(value)
            return value

        if isinstance(o, Binary):
            return o.__str__()

        return super().default(o)
