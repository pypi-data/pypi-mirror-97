from pydantic import BaseModel
from typing import List

class Attribute(BaseModel):
    key: str
    value: str

class FeatureAttributes(BaseModel):
    featureId: int
    attributes: dict

class FeatureAttributesLog(BaseModel):
    featureId: int
    attributes: List[dict]

class FeatureAttributeBulkCreate(BaseModel):
    featureId: int
    attributes: List[Attribute]