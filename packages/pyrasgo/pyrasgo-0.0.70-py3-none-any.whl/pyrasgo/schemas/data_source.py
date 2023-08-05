from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DataSourceBase(BaseModel):
    id: int


class DataSourceParent(DataSourceBase):
    id: Optional[int]
    name: Optional[str]
    table: Optional[str]
    tableDatabase: Optional[str]
    tableSchema: Optional[str]
    sourceType: Optional[str]
    domain: Optional[str]
    authorId: Optional[int]


class DataSource(DataSourceBase):
    id: Optional[int]
    name: Optional[str]
    organizationId: Optional[int]
    table: Optional[str]
    tableDatabase: Optional[str]
    tableSchema: Optional[str]
    sourceType: Optional[str]
    domain: Optional[str]
    authorId: Optional[int]
    tableStatus: Optional[str]
    parentId: Optional[int]
    parentSource: Optional[DataSourceParent]
    createdDate: Optional[str]


class DataSourceCreate(BaseModel):
    name: str
    table: Optional[str]
    tableDatabase: Optional[str]
    tableSchema: Optional[str]
    sourceType: Optional[str]
    domain: Optional[str]
    tableStatus: Optional[str]
    parentId: Optional[int]


class DataSourceUpdate(BaseModel):
    name: Optional[str]
    table: Optional[str]
    tableDatabase: Optional[str]
    tableSchema: Optional[str]
    sourceType: Optional[str]
    domain: Optional[str]
    tableStatus: Optional[str]
    parentId: Optional[int]