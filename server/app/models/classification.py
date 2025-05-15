import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import JSONB

from sqladmin import ModelView
from app.db import Base
from .dataset import Dataset

class Classification(Base):
    __tablename__ = 'classifications'
    
    hash:               Mapped[str] = mapped_column(primary_key=True, unique=True)
    dataset_id:         Mapped[id] = mapped_column(
                                sa.ForeignKey(Dataset.id, ondelete='CASCADE', onupdate='CASCADE'),
                                primary_key=True, 
                                index=True
                    )
    vectorizer:         Mapped[str]
    vectorizer_args:    Mapped[dict] = mapped_column(JSONB)
    classifier:         Mapped[str]
    classifier_args:    Mapped[dict] = mapped_column(JSONB)
    test_size:          Mapped[float]
    
    description:        Mapped[str | None]
    report:             Mapped[dict | None] = mapped_column(JSONB)
    
    
    dataset:            Mapped[Dataset] = relationship(back_populates='classifications')
    
    folds:              Mapped[list['ClassificationFold']] = relationship(
                            back_populates='classification', 
                            cascade='all, delete',
                            order_by="ClassificationFold.fold_num",
                        )
    
    
    
class ClassificationAdmin(ModelView, model=Classification):
    pass