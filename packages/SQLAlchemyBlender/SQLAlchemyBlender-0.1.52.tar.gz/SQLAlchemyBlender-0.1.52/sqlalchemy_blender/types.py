import uuid

from sqlalchemy.dialects.mysql.base import MSBinary
from sqlalchemy import types


class UUID(types.TypeDecorator):
    @property
    def python_type(self):
        pass

    def process_literal_param(self, value, dialect):
        pass

    impl = MSBinary

    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self,length=self.impl.length)

    def process_bind_param(self,value,dialect=None):
        if value and isinstance(value,uuid.UUID):
            return value.bytes
        elif value and not isinstance(value,uuid.UUID):
            raise ValueError(f'{value} is not a valid uuid.UUID')
        else:
            return None

    def process_result_value(self,value,dialect=None):
        if value:
            return uuid.UUID(bytes=value)
        else:
            return None

    def is_mutable(self):
        return False
