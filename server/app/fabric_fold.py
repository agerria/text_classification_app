import pickle
from typing import Type
import numpy as np
from sklearn.calibration import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.manifold import TSNE
from time import time
from pathlib import Path

from sklearn.neighbors import KDTree


from app.hash_json import hash_json

from app.translators.db_dataset_fold import DBDatasetFoldTraslator
from app.vectorizers.base import BaseVertorizer
from app.classificators.base import BaseClassifier
from app.logic.fold.consts import FoldType


class PredictorFabricFold:
    def __init__(
        self, 
        translator          : DBDatasetFoldTraslator,
        fold_type           : FoldType, 
        fold_num            : int,
        Vectorizer          : Type[BaseVertorizer],
        Classifier          : Type[BaseClassifier],
        vectorizer_kwargs   : dict = {},
        classifier_kwargs   : dict = {},
    ):
        self.translator = translator
        self.vectorizer = Vectorizer(**vectorizer_kwargs)
        self.classificator = Classifier(**classifier_kwargs)
        
        self.times = []
        self._start()
        self.translator.load_data(fold_type, fold_num)
        self._next('Загрузка данных')
        
        self.vectorized_texts = self.vectorizer.fit_transform(self.translator.texts)
        self._next('Векторизация')
        
        self._set_test_split()
        self._next('Разбиение')
        
        self.classificator.fit(self.train_texts, self.train_classes)
        self._next('Обучение')
        
        self.predicts = self.classificator.predict(self.test_texts)
        self._next('Классификация')
    
        self._end()
        
    
    def _set_test_split(self):
        self.test_texts = self.vectorized_texts[:self.translator.test_count]
        self.train_texts = self.vectorized_texts[self.translator.test_count:]
        
        self.test_classes = self.translator.classes[:self.translator.test_count]
        self.train_classes = self.translator.classes[self.translator.test_count:]
    
    
    def get_table_report(self, to_dict=True):
        data =  classification_report(self.test_classes, self.predicts, output_dict=to_dict, zero_division=0)
        if to_dict:
            for key in data.keys():
                if isinstance(data[key], dict) and 'f1-score' in data[key]:
                    data[key]['f1score'] = data[key].pop('f1-score')
        return data
    
    def get_predicts_vector(self):
        test_classes = self.test_classes
        predicts = self.predicts

        classes = sorted(list(set(self.translator.classes)))
        
        class_to_code = {cls: idx for idx, cls in enumerate(classes)}
        
        encoded_test = [class_to_code[c] for c in test_classes]
        encoded_predicts = [class_to_code[c] for c in predicts]
        
        return {
            "classes": classes,
            "test": encoded_test,
            "predicts": encoded_predicts
        }
        
    
    def get_report(self):
        return {
            'table': self.get_table_report(),
            'times': self.times,
        }
    
    
    
    def _start(self):
        self._start_time = self._current_time = self._prev_time = time()
        print('Старт')
        
    def _next(self, label):
        self._current_time = time()
        dt = self._current_time - self._prev_time
        self.times.append((label, dt))
        print(label, dt, flush=True)
        self._prev_time = self._current_time
        
    def _end(self):
        self._current_time = time()
        dt = self._current_time - self._start_time
        self.times.append(('Общее время', dt))
        print('Общее время', dt)
        