from typing import Self
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.models import Classification
from .classifications import ClassificationLogic
from ..views.classification.consts import CLASSIFIERS_SCHEME, VECTORIZERS_SCHEME
from .report import ReportMaker

class SIndicator(BaseModel):
    key: str
    label: str
    compareType: str
    dimension: str = ''
    isDatasetClass: bool = False
    children: list[Self] = []

class ClassificationTitle:
    def __init__(self, clsf: Classification):
        self.clsf = clsf

    def get_data(self):
        return {
            'hash': self.clsf.hash,
            'dataset': self.title_dataset,
            'vectorizer': self.title_vectorizer,
            'classifier': self.title_classifier,
        }
    
    
    @property
    def title_dataset(self):
        return {
            'title': self.clsf.dataset.name,
            'id': self.clsf.dataset_id,
        }
    
        
    @property
    def title_vectorizer(self):
        return self._unpack_args(self.clsf.vectorizer, self.clsf.vectorizer_args, VECTORIZERS_SCHEME)
    
    
    @property
    def title_classifier(self):
        return self._unpack_args(self.clsf.classifier, self.clsf.classifier_args, CLASSIFIERS_SCHEME)
    
    
    def _unpack_args(self, title, args, scheme):
        return {
            'title': title,
            'args': args,
        }
    
            



class ComparisonLogic:
    @classmethod
    def get_classification_info(cls, db: Session, hash: str):
        clsf = ClassificationLogic.get_classification(db, hash)
        title = ClassificationTitle(clsf)
        report = ReportMaker(clsf)
        
        return {
            'hash': clsf.hash,
            'title': title.get_data(),
            'indicators': report.get_data(),
        }
        
        
    @classmethod
    def get_indicators(cls, db: Session, hash: str):
        clsf = ClassificationLogic.get_classification(db, hash)
        report = ReportMaker(clsf)
        return report.get_indicators()
    
    
    