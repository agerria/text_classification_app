# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report


# from collections import Counter
# from traslators.csv import CsvTraslator
# from vectorizers.tfidf import TfIdfVectorizer
# from classificators.knn import KNNClassificator


# translator = CsvTraslator('Message', 'Category')
# translator.load_from_file("hf://datasets/prithivMLmods/Spam-Text-Detect-Analysis/Spam-Text-Detect-Analysis.csv")

# print(translator.classes)
# print(type(translator.classes))
# translator.classes = [
#     f'{cls}{i % 3}'
#     for i, cls in enumerate(translator.classes)
# ]

# vectorizer = TfIdfVectorizer()
# vec_texts = vectorizer.fit_transform(translator.texts)

# train_texts, test_texts, train_classes,  test_classes = train_test_split(vec_texts, translator.classes, test_size=0.2, random_state=42)

# classificator = KNNClassificator(9)
# classificator.fit(train_texts, train_classes)

# predicts = classificator.predict(test_texts)

# # print(*zip(predicts, test_classes), sep='\n')

# print(classification_report(test_classes, predicts))
# print(Counter(zip(predicts, test_classes)))

# # print(vec_texts)
# # print(vectorizer.vectorizer.get_feature_names_out())

import pickle

from typing import Type
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from time import time


from translators.base import BaseTraslator
from vectorizers.base import BaseVertorizer
from classificators.base import BaseClassifier

from classificators.knn import KNNClassifier
# from fabric import PredictorFabric
from translators import CsvTraslator
from vectorizers import TfIdfVectorizer

class PredictorFabric:
    def __init__(self):
        pass
    
    def create(
        self, 
        Translator          : Type[BaseTraslator],
        Vectorizer          : Type[BaseVertorizer],
        Classifier          : Type[BaseClassifier],
        translator_kwargs   : dict = {},
        vectorizer_kwargs   : dict = {},
        classifier_kwargs   : dict = {},
        test_size           : float = 0,
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
        
    
    def _set_test_split(self):
        (
            self.train_texts, 
            self.test_texts, 
            self.train_classes,  
            self.test_classes
        ) = train_test_split(self.vectorized_texts, self.translator.classes, test_size=self.test_size, random_state=42)
    
    
    def predict(self):
        pass
    
    
    def get_tests_report(self, to_dict=True):
        data =  classification_report(self.test_classes, self.predicts, output_dict=to_dict, zero_division=0)
        if to_dict:
            for key in data.keys():
                if isinstance(data[key], dict) and 'f1-score' in data[key]:
                    data[key]['f1score'] = data[key].pop('f1-score')
        self._next('Отчёт')
        return data
    
    
    
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




predictor = PredictorFabric()
predictor.create(
    CsvTraslator,
    TfIdfVectorizer,
    KNNClassifier,
    translator_kwargs = {
        'path': 'hf://datasets/prithivMLmods/Spam-Text-Detect-Analysis/Spam-Text-Detect-Analysis.csv',
        'text_column': 'Message',
        'class_column': 'Category',
    },
    vectorizer_kwargs = {},
    classifier_kwargs = {
        'neighbors_count': 3,
    },
    test_size = 0.2
)


predictor._end()
print(predictor.get_tests_report())


with open('predictor.pkl', 'wb') as fp:
    pickle.dump(predictor, fp)