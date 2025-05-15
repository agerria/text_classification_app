from sqlalchemy.orm import Session

from app.models import Classification
from app.shema.classification import (
    SClassificationOrm,
    SClassificationInfo
)

from .fold.consts import FoldType

class ClassificationLogic:
    @classmethod
    def add(cls, db: Session, s_orm: SClassificationOrm) -> Classification:
        classification = db.query(Classification).filter(
            Classification.hash == s_orm.hash,
        ).first()
        
        if not classification:
            classification = Classification(**s_orm.dict())
            db.add(classification)
        db.commit()
        
        return classification
    
    
    @classmethod
    def get_classification(cls, db: Session, hash) -> Classification:
        classification = db.query(Classification).filter(
            Classification.hash == hash,
        ).first()
        
        return classification
    
    @classmethod
    def delete_classification(cls, db: Session, hash):
        db.query(Classification).filter(
            Classification.hash == hash,
        ).delete()
        db.commit()
    
    
    @classmethod
    def save_report(cls, db: Session, classification: Classification, table, times):
        classification.report = {
            'table': table,
            'times': times,
        }
        db.commit()
        
    
    @classmethod
    def get_fold_reports(cls, db: Session, hash: str | None = None, classification: Classification | None = None) -> dict:
        if classification is None:
            classification = cls.get_classification(db, hash)
        
        fold_reports = {
            # t: []
            t: {
                n: None
                for n in range(1, classification.dataset.fold_count + 1)
            }
            for t in FoldType
        }
        
        for fold in classification.folds:
            # fold_reports[fold.fold_type].append(fold.report)
            fold_reports[fold.fold_type][fold.fold_num] = fold.report or {}
            
        return fold_reports
        
        
    
    @classmethod
    def get_report(cls, db: Session, hash: str | None = None, classification: Classification | None = None) -> dict:
        if classification is None:
            classification = cls.get_classification(db, hash)
        
        return classification.report
    
    
    @classmethod
    def get_settings(cls, db: Session, hash: str | None = None, classification: Classification | None = None) -> SClassificationOrm:
        if classification is None:
            classification = cls.get_classification(db, hash)
        
        return SClassificationOrm.from_orm(classification)
    
    @classmethod
    def get_info(cls, db: Session, hash: str | None = None, classification: Classification | None = None) -> SClassificationInfo:
        if classification is None:
            classification = cls.get_classification(db, hash)
            
        return SClassificationInfo(
            **cls.get_settings(db, classification=classification).dict(),
            dataset = classification.dataset.name,
        )