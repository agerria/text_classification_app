import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from sqladmin import ModelView
from app.db import Base

class Dataset(Base):
    __tablename__ = 'dataset'
    
    id:             Mapped[int] = mapped_column(primary_key=True)
    name:           Mapped[str]
    description:    Mapped[str | None]
    file:           Mapped[str]
    separator:      Mapped[str]
    class_header:   Mapped[str]
    data_header:    Mapped[str]
    fold_count:     Mapped[int] = mapped_column(server_default='5')
    
    rows:           Mapped[list['DatasetRow']] = relationship(back_populates='dataset', cascade='all, delete')
    classifications:Mapped[list['Classification']] = relationship(back_populates='dataset', cascade='all, delete')
    
    
    def __str__(self) -> str:
        return f'Датасет <{self.name}> - {self.id}'
    
class DatasetAdmin(ModelView, model=Dataset):
    column_list = [
        Dataset.id,
        Dataset.name,
        Dataset.file,
        Dataset.separator,
        Dataset.class_header,
        Dataset.data_header,
    ]