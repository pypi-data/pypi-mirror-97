from typing import List, Optional

from enum import Enum
from pydantic import BaseModel


class DataType(Enum):
    INT = 'int'
    INTEGER = 'integer'
    FLOAT = 'float'
    FLOAT64 = 'float64'
    DECIMAL = 'decimal'
    NUMERIC = 'numeric'
    NUMBER = 'number'
    REAL = 'real'
    DOUBLE = 'double'
    STRING = 'string'
    TEXT = 'text'
    VARCHAR = 'varchar'
    CHAR = 'char'
    DATE = 'date'
    DATETIME = 'datetime'
    TIMESTAMP = 'timestamp'
    BINARY = 'binary'
    BOOLEAN = 'boolean'
    BOOL = 'bool'

    @classmethod
    def __missing__(cls, key):
        formatted = key.replace(" ", "").lower()
        try:
            return cls._value2member_map_[formatted]
        except KeyError:
            raise ValueError("%r is not a valid %s" % (key, cls.__name__))


class Dimension(BaseModel):
    name: str
    data_type: DataType


class Feature(BaseModel):
    data_type: DataType
    name: str
    display_name: Optional[str] = ''
    description: Optional[str] = ''
    tags: Optional[List[str]]


class FeatureSet(BaseModel):
    name: Optional[str]
    script: Optional[str]
    table: str
    datasource: Optional[str]
    granularity: Optional[str]
    granularities: Optional[List[str]]
    dimensions: List[Dimension]
    features: List[Feature]
