from pydantic import computed_field
from .base import BaseModel

class STableOptions(BaseModel):
    limit: int
    page: int
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit