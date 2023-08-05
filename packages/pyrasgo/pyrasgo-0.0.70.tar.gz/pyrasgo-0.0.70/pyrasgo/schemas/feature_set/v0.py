from typing import Optional
from pydantic import BaseModel

from pyrasgo.schemas.data_source import DataSource


class FeatureSetBase(BaseModel):
    id: int


class FeatureSetCreate(BaseModel):
    name: str
    snowflakeTable: str
    dataSourceId: int
    rawFilePath: Optional[str]
    granularity: Optional[str]


class FeatureSetUpdate(BaseModel):
    id: int
    name: Optional[str]
    snowflakeTable: Optional[str]
    dataSourceId: Optional[int]
    rawFilePath: Optional[str]
    granularity: Optional[str]


class FeatureSet(FeatureSetBase):
    name: Optional[str]
    snowflakeTable: Optional[str]
    dataSource: Optional[DataSource]
    rawFilePath: Optional[str]
    granularity: Optional[str]
    organizationId: Optional[int]