from boto3.dynamodb.conditions import Key, ConditionExpressionBuilder, Attr
import re
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

ATTR_NAME_REGEX = re.compile(r'[^.\[\]]+(?![^\[]*\])')


class ExpressionBuilder(ConditionExpressionBuilder):
    def _build_value_placeholder(self, value, attribute_value_placeholders, is_resource=True,
                                 has_grouped_values=False):
        # If the values are grouped, we need to add a placeholder for
        # each element inside of the actual value.
        serializer = TypeSerializer()
        if has_grouped_values:
            placeholder_list = []
            for v in value:
                value_placeholder = self._get_value_placeholder()
                self._value_count += 1
                placeholder_list.append(value_placeholder)
                if is_resource:
                    attribute_value_placeholders[value_placeholder] = v
                else:
                    attribute_value_placeholders[value_placeholder] = serializer.serialize(v)
            # Assuming the values are grouped by parenthesis.
            # IN is the currently the only one that uses this so it maybe
            # needed to be changed in future.
            return '(' + ', '.join(placeholder_list) + ')'
        # Otherwise, treat the value as a single value that needs only
        # one placeholder.
        else:
            value_placeholder = self._get_value_placeholder()
            self._value_count += 1
            attribute_value_placeholders[value_placeholder] = serializer.serialize(value)
            return value_placeholder


class ConditionHandler:
    builder_class = ExpressionBuilder

    def __init__(self):
        self.builder = self.builder_class()

    def handle_condition(self, condition, is_resource=True, is_key=True):
        if is_resource:
            return condition

        built = self.builder.build_expression(condition, is_key_condition=is_key, is_resource=False)
        return {
            'KeyConditionExpression': built.condition_expression,
            'ExpressionAttributeNames': built.attribute_name_placeholders,
            'ExpressionAttributeValues': built.attribute_value_placeholders,
        }

    def build_condition(self, is_key=True, is_resource=True, **kwargs):
        method = Key if is_key else Attr
        condition = None
        for k, v in kwargs.items():
            key = k
            try:
                if k[-5:] == '__lte':
                    op = 'lte'
                    key = k[:-5]
                elif k[-5:] == '__gte':
                    op = 'gte'
                    key = k[:-5]
                elif k[-5:] == '__startswith':
                    op = 'begins_with'
                    key = k[:-5]
                else:
                    op = 'eq'
            except:
                op = 'eq'

            if not condition:
                condition = getattr(method(key), op)(v)
            else:
                condition = condition & getattr(method(key), op)(v)
        condition = self.handle_condition(condition, is_resource)
        return condition
