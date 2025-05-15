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

from app.translators.base import BaseTraslator
from app.vectorizers.base import BaseVertorizer
from app.classificators.base import BaseClassifier

from app.shema.fabric import (
    SContourData,
    SDecisionBoundaryData,
    SPointData,
)

class PredictorFabric:
    DUMPS_DIR = Path('predictor_dumps/')
    
    def __init__(
        self, 
        Translator          : Type[BaseTraslator],
        Vectorizer          : Type[BaseVertorizer],
        Classifier          : Type[BaseClassifier],
        translator_kwargs   : dict = {},
        vectorizer_kwargs   : dict = {},
        classifier_kwargs   : dict = {},
        test_size           : float = 0,
        
        hash_form           : str = None,
        settings            : dict = None,
    ):
        self.translator = Translator(**translator_kwargs)
        self.vectorizer = Vectorizer(**vectorizer_kwargs)
        self.classificator = Classifier(**classifier_kwargs)
        self.test_size = test_size
        
        self.times = []
        self._start()
        self.translator.load_data()
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
        
        
        self._hash_form = hash_form
        self._settings = settings
        self.save_dump()
    
    def _set_test_split(self):
        (
            self.train_texts, 
            self.test_texts, 
            self.train_classes,  
            self.test_classes
        ) = train_test_split(self.vectorized_texts, self.translator.classes, test_size=self.test_size, random_state=42)    
    
    def predict(self):
        pass
    
    
    def get_table_report(self, to_dict=True):
        data =  classification_report(self.test_classes, self.predicts, output_dict=to_dict, zero_division=0)
        if to_dict:
            for key in data.keys():
                if isinstance(data[key], dict) and 'f1-score' in data[key]:
                    data[key]['f1score'] = data[key].pop('f1-score')
        return data
    
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
    


    def get_tsne_data(self) -> SDecisionBoundaryData:
        tsne = TSNE(n_components=2, random_state=4)
        
        X = tsne.fit_transform(self.train_texts.toarray())
        y = self.train_classes
        
        X_predict = tsne.fit_transform(self.test_texts.toarray())
        y_predict = self.predicts

        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
        y_predict_encoded = label_encoder.transform(y_predict)

        # Создание сетки для контурного графика
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 10),
                            np.linspace(y_min, y_max, 10))

        # Преобразование сетки в список точек
        grid_points = np.c_[xx.ravel(), yy.ravel()]

        # Создание дерева ближайших соседей
        tree = KDTree(X)

        # Поиск ближайших точек и их классов
        distances, indices = tree.query(grid_points, k=1)
        Z = y_encoded[indices].reshape(xx.shape)

        # Упаковка данных в Pydantic объекты
        contour_data = SContourData(
            xx=xx[0].tolist(),
            yy=yy[:, 0].tolist(),
            Z=Z.tolist()
        )

        training_points = SPointData(
            x=X[:, 0].tolist(),
            y=X[:, 1].tolist(),
            classes=y_encoded.tolist(),
            names=y,
        )

        test_points = SPointData(
            x=X_predict[:, 0].tolist(),
            y=X_predict[:, 1].tolist(),
            classes=y_predict_encoded.tolist(),
            names=y_predict,
        )

        decision_boundary_data = SDecisionBoundaryData(
            contour=contour_data,
            training_points=training_points,
            test_points=test_points
        )
        return decision_boundary_data
        
        
    def save_dump(self):
        if self._hash_form is None:
            return
        
        self.DUMPS_DIR.mkdir(exist_ok=True)
        filename = self.dump_name(self._hash_form)
        
        with open(filename, 'wb') as fp:
            pickle.dump(self, fp)
            
            
    @classmethod
    def check_dump_exist(cls, hash) -> bool:
        return cls.dump_name(hash).exists()
    
    @classmethod
    def dump_name(cls, hash) -> Path:
        return  cls.DUMPS_DIR / hash
    
    @classmethod
    def load_dump(cls, hash):
        dumpname = cls.dump_name(hash)
        try:
            with open(dumpname, 'rb') as fp:
                obj = pickle.load(fp)
            return obj
        except:
            dumpname.unlink()
            return
        