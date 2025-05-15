from typing import Any
from pydantic import Field
from .base import BaseModel, OrmModel

class SClassificationSchemaArg(BaseModel):
    key: str
    label: str
    type: str
    default: Any = Field(None)
    variants: list[str] = Field(None)
    
class SClassificationSchemaItem(BaseModel):
    value: str
    label: str
    args: list[SClassificationSchemaArg] = []
    
class SClassificationSchema(BaseModel):
    vectorizers: list[SClassificationSchemaItem] = []
    classifiers: list[SClassificationSchemaItem] = []
    
class SClassificationDataset(BaseModel):
    value: int
    label: str
    filename: str
    id: int
    
class SClassificationRun(BaseModel):
    dataset_id: int
    vectorizer: str
    classifier: str
    vectorizer_args: dict
    classifier_args: dict
    test_size: float
    
class SClassificationOrm(SClassificationRun, OrmModel):
    hash: str
    report: dict | None = None
    description: str | None = None
    
    
class SClassificationInfo(SClassificationOrm):
    dataset: str
    
    