from sqlalchemy.orm import Session

from app import task_queue
from app.db import get_db, SessionLocal
from app.models import Classification, ClassificationFold
from app.fabric import PredictorFabric
from app.fabric_fold import PredictorFabricFold
from app.translators.db_dataset_fold import DBDatasetFoldTraslator
from app.translators.db_dataset import DBDatasetTraslator
from app.logic.fold.consts import FoldType
from app.logic.classifications import ClassificationLogic
from app.views.classification.consts import VECTORIZERS_SCHEME, CLASSIFIERS_SCHEME


def get_fold(db: Session, hash, type, num) -> ClassificationFold:
    fold = db.query(ClassificationFold).get((hash, num, type))
    if not fold:
        fold = ClassificationFold(
            classification_hash = hash,
            fold_type = type,
            fold_num = num,
        )
        db.add(fold)
    
    return fold

def run_predict_folds(clsf: Classification):
    fold_count = clsf.dataset.fold_count
    db = SessionLocal()
    
    if not clsf.report:
        job = task_queue.enqueue(run_predict_base_fold, clsf=clsf)
        print('RUN BASE', job)
    
    
    folds: list[ClassificationFold] = []
    for fold_type in FoldType:
        for fold_num in range(1, fold_count + 1):
            fold = get_fold(db, clsf.hash, fold_type, fold_num)
            folds.append(fold)
    db.commit()
    
    for fold in folds:
        if fold.report:
            continue
        job = task_queue.enqueue(run_predict_fold, fold=fold)
        print('RUN', fold, job)
        

def run_predict_fold(fold: ClassificationFold) -> PredictorFabricFold:
    db = SessionLocal()
    fold = db.merge(fold)
    
    clsf = fold.classification    
    translator = DBDatasetFoldTraslator(db, clsf.dataset_id)
    
    
    Vectorizer = VECTORIZERS_SCHEME[clsf.vectorizer]['class']
    Classifier = CLASSIFIERS_SCHEME[clsf.classifier]['class']
    
    fabric = PredictorFabricFold(
        translator = translator,
        fold_type = fold.fold_type,
        fold_num = fold.fold_num,
        Vectorizer = Vectorizer,
        vectorizer_kwargs = clsf.vectorizer_args,
        Classifier = Classifier,
        classifier_kwargs = clsf.classifier_args,
    )
    
    fold.report = fabric.get_report()
    if fold.fold_num == 1:
        fold.report['predicts'] = fabric.get_predicts_vector()
    db.commit()
    
    return fabric


def run_predict_base_fold(clsf: Classification):
    db = SessionLocal()
    clsf = db.merge(clsf)
    
    translator_args = {
        'db': db,
        'dataset_id': clsf.dataset_id,
    }
    
    Vectorizer = VECTORIZERS_SCHEME[clsf.vectorizer]['class']
    Classifier = CLASSIFIERS_SCHEME[clsf.classifier]['class']
    
    fabric = PredictorFabric(
        Translator = DBDatasetTraslator,
        translator_kwargs = translator_args,
        Vectorizer = Vectorizer,
        vectorizer_kwargs = clsf.vectorizer_args,
        Classifier = Classifier,
        classifier_kwargs = clsf.classifier_args,
        test_size = clsf.test_size,
        
        hash_form = None,
    )
    
    clsf.report = fabric.get_report()
    db.commit()
    print('clsf', clsf, clsf.report, clsf.hash, sep='\n')
    
    # table = fabric.get_tests_report()
    # ClassificationLogic.save_report(
    #     db,
    #     clsf,
    #     table,
    #     fabric.times,
    # )