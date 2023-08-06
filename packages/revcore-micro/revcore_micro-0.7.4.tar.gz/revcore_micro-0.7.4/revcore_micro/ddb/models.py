import boto3
from boto3.dynamodb.conditions import Key, Attr
from uuid import uuid4
from boto3.dynamodb.types import Decimal, Binary
from datetime import datetime
import time
from revcore_micro.ddb import exceptions
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from revcore_micro.ddb.conditions import ConditionHandler
import json
from revcore_micro.utils import DecimalEncoder

condition_builder = ConditionHandler()


class Model:
    table_name = None
    region = 'ap-northeast-1'
    partition_key = None
    partition_type = 'S'
    sort_key = None
    sort_type = 'S'
    s_indexes = {}
    g_indexes = {}
    condition_handler = ConditionHandler()

    @classmethod
    def init_table(cls):
        client = boto3.client('dynamodb', region_name=cls.region)
        try:
            response = client.describe_table(
                TableName=cls.table_name
            )
        except:
            key_schema = [{'AttributeName': cls.partition_key, 'KeyType': 'HASH'}]
            attrs = [{'AttributeName': cls.partition_key, 'AttributeType': cls.partition_type}]

            if cls.sort_key:
                key_schema.append({'AttributeName': cls.sort_key, 'KeyType': 'RANGE'})
                attrs.append({'AttributeName': cls.sort_key, 'AttributeType': cls.sort_type})

            indexes = []
            gindexes = []
            kwargs = {'TableName': cls.table_name, 'KeySchema': key_schema, 'AttributeDefinitions': attrs, 'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }}

            for key, value in cls.s_indexes.items():
                schemas = [{'AttributeName': value['pkey'], 'KeyType': 'HASH'}]
                if not [attr for attr in attrs if attr['AttributeName'] == value['pkey']]:
                    attrs.append({'AttributeName': value['pkey'], 'AttributeType': value.get('ptype', 'S')})
                if value.get('skey'):
                    schemas.append({'AttributeName': value['skey'], 'KeyType': 'RANGE'})
                    if not [attr for attr in attrs if attr['AttributeName'] == value['skey']]:
                        attrs.append({'AttributeName': value['skey'], 'AttributeType': value.get('stype', 'S')})
                indexes.append({'IndexName': key, 'KeySchema': schemas, 'Projection': {'ProjectionType': 'ALL'}})
            for key, value in cls.g_indexes.items():
                schemas = [{'AttributeName': value['pkey'], 'KeyType': 'HASH'}]
                if not [attr for attr in attrs if attr['AttributeName'] == value['pkey']]:
                    attrs.append({'AttributeName': value['pkey'], 'AttributeType': value.get('ptype', 'S')})
                if value.get('skey'):
                    schemas.append({'AttributeName': value['skey'], 'KeyType': 'RANGE'})
                    if not [attr for attr in attrs if attr['AttributeName'] == value['skey']]:
                        attrs.append({'AttributeName': value['skey'], 'AttributeType': value.get('stype', 'S')})
                gindexes.append({'IndexName': key, 'KeySchema': schemas, 'Projection': {'ProjectionType': 'ALL'}, 'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}})
            

            if indexes:
                kwargs['LocalSecondaryIndexes'] = indexes

            if gindexes:
                kwargs['GlobalSecondaryIndexes'] = gindexes

            response = client.create_table(
                **kwargs
            )

    @classmethod
    def build_condition(cls, is_key=True, **kwargs):
        condition = cls.condition_handler.build_condition(is_key=is_key, **kwargs)
        return condition

    @classmethod
    def _get_client(cls, page=False):
        client = boto3.resource('dynamodb', region_name=cls.region)
        return client.Table(cls.table_name)

    @classmethod
    def get(cls, **kwargs):
        client = cls._get_client()
        key = {
            cls.partition_key: kwargs[cls.partition_key],
        }
        if cls.sort_key:
            key[cls.sort_key] = kwargs[cls.sort_key]
        try:
            resp = client.get_item(Key=key)
            return cls.deserialize(resp['Item'])
        except KeyError:
            raise exceptions.InstanceNotFound(table_name=cls.table_name, key=key)

    @classmethod
    def put(cls, **kwargs):
        client = cls._get_client()
        data = cls.serialize(kwargs)
        timestamp = int(datetime.now().timestamp())
        pk = f'{timestamp}-{uuid4().hex}'
        key = {
            cls.partition_key: kwargs.pop(cls.partition_key, pk)
        }
        if cls.sort_key:
            key[cls.sort_key] = kwargs.pop(cls.sort_key, pk)
        items = {
            'created': {
                'Value': kwargs.pop('timestamp', timestamp),
                'Action': 'PUT'
            },
            'updated': {
                'Value': timestamp,
                'Action': 'PUT'
            }
        }
        for k, v in data.items():
            items[k] = {
                'Value': v,
                'Action': 'PUT'
            }
        resp = client.update_item(Key=key,
                                  AttributeUpdates=items,
                                  ReturnValues='ALL_NEW')
        return cls.deserialize(resp['Attributes'])

    @classmethod
    def delete(cls, **kwargs):
        client = cls._get_client()
        key = {
            cls.partition_key: kwargs[cls.partition_key],
        }
        if cls.sort_key:
            key[cls.sort_key] = kwargs[cls.sort_key]
        resp = client.delete_item(Key=key)

    @classmethod
    def query(cls, index_name=None, limit=60, last_key=None, **kwargs):
        client = cls._get_client()
        condition = cls.build_condition(**kwargs)
        extra = {'KeyConditionExpression': condition, 'Limit': limit}
        if index_name:
            extra['IndexName'] = index_name

        if last_key:
            extra['ExclusiveStartKey'] = last_key
        resp = client.query(**extra)
        return cls.deserialize(resp['Items'])

    @classmethod
    def filter_query(cls, key_condition, index_name=None, **kwargs):
        client = cls._get_client()
        condition = cls.build_condition(is_key=False, **kwargs)
        k_condition = cls.build_condition(**key_condition)
        extra = {
            'KeyConditionExpression': k_condition,
            'FilterExpression': condition,
        }
        if index_name:
            extra['IndexName'] = index_name
        resp = client.query(**extra)
        return resp['Items']

    @classmethod
    def batch_write(cls, items: list):
        client = cls._get_client()
        result = []
        with client.batch_writer() as batch:
            for item in items:
                _item = {
                    cls.partition_key: uuid4().hex,
                }
                if cls.sort_key:
                    _item[cls.sort_key] = uuid4().hex
                _item = {
                    **_item,
                    **item
                }
                batch.put_item(Item=_item)
                result.append(_item)
        return result

    @staticmethod
    def serialize(data):
        for k, v in data.items():
            if isinstance(v, float):
                data[k] = Decimal(v)
            elif isinstance(v, dict):
                data[k] = Model.serialize(v)

        return data

    @staticmethod
    def deserialize(data):
        deserialize_str = json.dumps(data, cls=DecimalEncoder)
        return json.loads(deserialize_str)

    @classmethod
    def scan(cls, **kwargs):
        client = cls._get_client()
        resp = client.scan(**kwargs)
        return resp

    @classmethod
    def clean_up(cls, **kwargs):
        client = cls._get_client()
        scan = cls.scan()
        with client.batch_writer() as batch:
            for each in scan:
                key = {
                    cls.partition_key: each[cls.partition_key]
                }
                if cls.sort_key:
                    key[cls.sort_key] = each[cls.sort_key]

                batch.delete_item(
                    Key=key,
                )


class BigModel(Model):
    model = None
    partition_key = 'model'
    sort_key = 'id'
    table_name = None

    @classmethod
    def get(cls, **kwargs):
        kwargs['model'] = cls.model
        return super(BigModel, cls).get(**kwargs)

    @classmethod
    def delete(cls, **kwargs):
        kwargs['model'] = cls.model
        return super(BigModel, cls).delete(**kwargs)

    @classmethod
    def put(cls, **kwargs):
        kwargs['model'] = cls.model
        return super(BigModel, cls).put(**kwargs)

    @classmethod
    def query(cls, index_name=None, **kwargs):
        kwargs['model'] = cls.model
        return super(BigModel, cls).query(**kwargs, index_name=index_name)

    @classmethod
    def filter_query(cls, key_condition, index_name=None, **kwargs):
        key_condition['model'] = cls.model
        return super(BigModel, cls).filter_query(**kwargs, index_name=index_name, key_condition=key_condition)

    @classmethod
    def batch_write(cls, items: list):
        items = list(map(lambda _item: {**_item, 'model': cls.model}, items))
        return super(BigModel, cls).batch_write(items)
