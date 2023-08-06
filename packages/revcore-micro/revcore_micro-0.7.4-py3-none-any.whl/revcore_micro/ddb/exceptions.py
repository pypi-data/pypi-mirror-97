class ModelException(Exception):
    pass


class InstanceNotFound(ModelException):
    def __init__(self, table_name, key):
        self.table_name = table_name
        self.key = key
        key_msg = ','.join([f'{k}: v' for k, v in key.items()])
        self.msg = f'Table {table_name} not found with {key_msg}'

        super().__init__(self.msg)
