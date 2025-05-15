import json
from fastapi import Depends
from fastapi_utils.cbv import cbv

from pydantic import BaseModel
from sqlalchemy import func


from . import router
from app.auth import AuthView

from app.models import Dataset, Classification

from app.shema.classification import (
    SClassificationDataset,
    SClassificationRun, 
    SClassificationSchema, 
    SClassificationSchemaArg, 
    SClassificationSchemaItem,
    SClassificationOrm,
)


from app.fabric import PredictorFabric
from app.translators.db_dataset import DBDatasetTraslator
from app.logic.classifications import ClassificationLogic

from .consts import CLASSIFIERS_SCHEME, VECTORIZERS_SCHEME

from app.hash_json import hash_json

class SHash(BaseModel):
    calc_hash: str

@cbv(router)
class ClassificationView(AuthView):
    @router.get('/schemes/')
    async def schemes(self) -> SClassificationSchema:
        return self.get_schemes()
    
    
    @router.get('/datasets/')
    async def datasets(self) -> list[SClassificationDataset]:
        datasets = self.db.query(
            Dataset.id.label('value'),
            Dataset.name.label('label'),
            Dataset.file.label('filename'),
            Dataset.id
        )
        
        data = [
            SClassificationDataset(**dataset._asdict())
            # dataset._asdict()
            for dataset in datasets
        ]
        
        print(data)
        
        return data
    
    @router.post('/calculate/')
    async def calculate(self, settings: SClassificationRun):
        hash_form = hash_json(settings)
        print('-->', settings)
        classification = ClassificationLogic.add(
            self.db,
            SClassificationOrm(
                **settings.dict(),
                hash = hash_form,
            )
        )
        
        # fabric = None
        # if PredictorFabric.check_dump_exist(hash_form):
        #     fabric: PredictorFabric = PredictorFabric.load_dump(hash_form)
        
        # if fabric is None:
        #     translator_args = {
        #         'db': self.db,
        #         'dataset_id': settings.dataset_id,
        #     }
            
        #     Vectorizer = VECTORIZERS_SCHEME[settings.vectorizer]['class']
        #     Classifier = CLASSIFIERS_SCHEME[settings.classifier]['class']
            
        #     fabric = PredictorFabric(
        #         Translator = DBDatasetTraslator,
        #         translator_kwargs = translator_args,
        #         Vectorizer = Vectorizer,
        #         vectorizer_kwargs = settings.vectorizer_args,
        #         Classifier = Classifier,
        #         classifier_kwargs = settings.classifier_args,
        #         test_size = settings.test_size,
                
        #         hash_form = hash_form,
        #         settings = settings,
        #     )
        
        # table = fabric.get_tests_report()
        # print(fabric.get_tests_report(to_dict=False))
        
        # print('------------')
        
        # ClassificationLogic.save_report(
        #     self.db,
        #     classification,
        #     table,
        #     fabric.times,
        # )
        from app.logic.fold.fabric import run_predict_folds
        run_predict_folds(classification)
        return classification.hash
        return classification.report
         
        data = {
            'table': table,
            'times': fabric.times,
            # 'calc_hash': hash_form,
        }
        
        return data
    
    
    @router.get('/calculate/{hash_form}')
    async def get_calculate(self, hash_form:str):
        classification = ClassificationLogic.get_classification(self.db, hash_form)
        if not classification:
            return None
        
        data = {
            'report': ClassificationLogic.get_report(self.db, classification=classification),
            'settings': ClassificationLogic.get_settings(self.db, classification=classification),
            'folds': ClassificationLogic.get_fold_reports(self.db, classification=classification)
        }
        
        return data
    
    
    @router.delete('/calculate/{hash_form}')
    async def delete_calculate(self, hash_form:str):
        ClassificationLogic.delete_classification(self.db, hash_form)
        return {}
    
    
    
    @router.post('/chart/')
    async def chart(self, hash: SHash):
        fabric: PredictorFabric = PredictorFabric.load_dump(hash.calc_hash)
        chart = fabric.get_tsne_data()
        return chart
        
    
    
    
    
    @classmethod
    def get_schemes(cls) -> SClassificationSchema:
        schemes = SClassificationSchema()
        schemes.vectorizers = cls.get_scheme(VECTORIZERS_SCHEME)
        schemes.classifiers = cls.get_scheme(CLASSIFIERS_SCHEME)
        return schemes
    
    @classmethod
    def get_scheme(cls, scheme: dict) -> list[SClassificationSchemaItem]:
        data = []
        for key, v in scheme.items():
            item = SClassificationSchemaItem(value=key, label=v['label'])
            
            for arg in v['args']:
                item.args.append(
                    SClassificationSchemaArg(**arg)
                )
            data.append(item)
        return data
    
    
    