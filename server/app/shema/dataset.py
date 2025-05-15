from typing import Optional

from .base import BaseModel, OrmModel

class SDatasetAdd(BaseModel):
    name:  str
    description: str | None
    file:  str
    separator:  str
    class_header:  str
    data_header:  str
    

class SDatasetTableRow(BaseModel):
    id: int
    name: str
    description: str | None
    
    class_count: int
    rows_count: int
    # class_rows: list[tuple[str, int]]
    
    
class SDatasetTable(BaseModel):
    data: list[SDatasetTableRow]
    total: int
    

class SDatasetClass(BaseModel):
    name: str
    rows_count: int
    percent: float
        

class SDatasetInfo(SDatasetAdd, OrmModel):
    id: int
    rows_count: int = 0
    classes: list[SDatasetClass] = []


class SDatasetRowTableRow(OrmModel):
    num: int
    classname: str
    text: str

class SDatasetRowTable(BaseModel):
    data: list[SDatasetRowTableRow]
    total: int
    