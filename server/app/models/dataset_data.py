import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from sqladmin import ModelView
from app.db import Base
from .dataset import Dataset

class DatasetRow(Base):
    __tablename__ = 'dataset_row'
    
    dataset_id:     Mapped[str] = mapped_column(
                                sa.ForeignKey(Dataset.id, ondelete='CASCADE', onupdate='CASCADE'),
                                primary_key=True, 
                                index=True
                    )
    num:            Mapped[int] = mapped_column(primary_key=True, unique=False, index=True)
    classname:      Mapped[str] = mapped_column(index=True)
    text:           Mapped[str]
    
    dataset:        Mapped[Dataset] = relationship(back_populates='rows')
    
    random_fold:    Mapped[int | None] = mapped_column(index=True)
    stratified_fold:Mapped[int | None] = mapped_column(index=True)
    
    def __str__(self) -> str:
        return f'{self.classname} - {self.text}'
    
    
class DatasetRowAdmin(ModelView, model=DatasetRow):
    column_list = [
        DatasetRow.dataset_id,
        DatasetRow.num,
        DatasetRow.classname,
        DatasetRow.text,
    ]
    form_excluded_columns = [DatasetRow.dataset_id]
    form_include_pk = True
    
    