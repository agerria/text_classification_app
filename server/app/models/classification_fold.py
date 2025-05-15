import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from sqladmin import ModelView
from app.db import Base
from .classification import Classification
from app.logic.fold.consts import FoldType

class ClassificationFold(Base):
    __tablename__ = 'classification_folds'
    
    classification_hash:    Mapped[str] = mapped_column(
                                sa.ForeignKey(Classification.hash, ondelete='CASCADE', onupdate='CASCADE'),
                                primary_key=True, 
                                index=True
                    )
    fold_num:  Mapped[int] = mapped_column(primary_key=True, index=True)
    fold_type: Mapped[FoldType] = mapped_column(primary_key=True, index=True)
    
    report:    Mapped[dict | None] = mapped_column(JSONB)
    
    
    classification: Mapped[Classification] = relationship(back_populates='folds')
    
    
    