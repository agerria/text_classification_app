from typing import Optional
from pydantic import  model_validator


from .base import BaseModel, OrmModel
from .classification import SClassificationOrm    

class SCompoarisonTableRow(BaseModel):
    key: str
    hash: str
    dataset: str
    dataset_id: int
    vectorizer: str
    classifier: str

    
    
class SComparisonTable(BaseModel):
    data: list[SCompoarisonTableRow]
    total: int
    

class SIComparisonInfo(BaseModel):
    hashs: list[str]