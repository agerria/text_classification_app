
# from app.classificators.bayes import MyNBClassifier, NBClassifier
# from app.classificators.decision_tree import DTClassifier
# from app.classificators.knn import KNNClassifier, MyKNNClassifier
# from app.classificators.svm import SVMClassifier
# from app.classificators.logistic_regression import LRClassifier
from app.classificators import *
from app.vectorizers import (
    TfIdfVectorizer,
    BagOfWordsVectorizer,
    FastTextVectorizer,
)


CLASSIFIERS_SCHEME = {
    'KNNClassifier': {
        'class': KNNClassifier,
        'label': 'KNNClassifier',
        'args':[
            {
                'key': 'neighbors_count',
                'label': 'Количество соседей',
                'default': 3,
                'type': 'int'
            },
            {
                'key': 'metric',
                'label': 'Метрика близости',
                'type': 'select',
                'default': 'euclidean',
                'variants': [
                    # 'correlation',
                    # 'cosine',
                    # 'euclidean', # default
                    # 'minkowski'
                    
                    'cosine', 
                    'l1', 
                    'l2', 
                    'cityblock', 
                    'manhattan', 
                    'euclidean',
                ]
            }
        ]
    },
    'MyKNNClassifier': {
        'class': MyKNNClassifier,
        'label': 'MyKNNClassifier',
        'args': [
            {
                'key': 'neighbors_count',
                'label': 'Количество соседей',
                'default': 3,
                'type': 'int'
            },
            {
                'key': 'metric',
                'label': 'Метрика близости',
                'type': 'select',
                'default': 'euclidean',
                'variants': [
                    # 'correlation',
                    # 'cosine',
                    # 'euclidean',  # default
                    # 'minkowski'
                    'cosine', 
                    'l1', 
                    'l2', 
                    'cityblock', 
                    'manhattan', 
                    'euclidean',
                ]
            }
        ]
    },
    'NBClassifier': {
        'class': NBClassifier,
        'label': 'NBClassifier',
        'args': [
            {
                'key': 'alpha',
                'label': 'Коэффициент сглаживания',
                'default': 1.0,
                'type': 'float'
            }
        ]
    },
    'MyNBClassifier': {
        'class': MyNBClassifier,
        'label': 'MyNBClassifier',
        'args': [
            {
                'key': 'alpha',
                'label': 'Коэффициент сглаживания',
                'default': 1.0,
                'type': 'float'
            }
        ]
    },
    'SVMClassifier': {
        'class': SVMClassifier,
        'label': 'SVMClassifier',
        'args': [
            {
                'key': 'C',
                'label': 'Параметр регуляризации',
                'default': 1.0,
                'type': 'float'
            },
            {
                'key': 'kernel',
                'label': 'Ядро',
                'type': 'select',
                'default': 'rbf',
                'variants': [
                    'linear',
                    'poly',
                    'rbf', # default
                    'sigmoid',
                    'precomputed'
                ]
            },
            {
                'key': 'random_state',
                'label': 'Зерно',
                'type': 'int'
            }
        ]
    },
    'DTClassifier': {
        'class': DTClassifier,
        'label': 'DTClassifier',
        'args': [
        ]
    },
    'LRClassifier': {
        'class': LRClassifier,
        'label': 'LRClassifier',
        'args': [
            {
                'key': 'C',
                'label': 'Сила регуляризации',
                'default': 1.0,
                'type': 'float',
                'description': 'Меньшие значения = сильнее регуляризация (1.0 по умолчанию)'
            },
            {
                'key': 'penalty',
                'label': 'Тип регуляризации',
                'type': 'select',
                'default': 'l2',
                'variants': ['l1', 'l2'],
                'description': 'L1 - отбор признаков, L2 - сглаживание весов'
            },
            {
                'key': 'class_weight',
                'label': 'Балансировка классов',
                'type': 'select',
                'default': None,
                'variants': ['balanced'],
                'description': 'Автоматическая балансировка весов классов'
            }
        ]
    },
    'RFClassifier': {
        'class': RFClassifier,
        'label': 'RFClassifier',
        'args': [
            {
                'key': 'n_estimators',
                'label': 'Число деревьев',
                'default': 100,
                'type': 'int',
                'description': 'Больше деревьев = стабильнее модель (100 по умолчанию)'
            },
            {
                'key': 'max_depth',
                'label': 'Макс. глубина',
                'default': None,
                'type': 'int',
                'description': 'Ограничение глубины деревьев (None = без ограничений)'
            },
            {
                'key': 'max_features',
                'label': 'Признаков на разделение',
                'type': 'select',
                'default': 'sqrt',
                'variants': ['sqrt', 'log2'],
                'description': 'Рекомендуется уменьшать для текстовых данных'
            }
        ]
    },
    'GBClassifier': {
        'class': GBClassifier,
        'label': 'GBClassifier',
        'args': [
            {
                'key': 'n_estimators',
                'label': 'Число деревьев',
                'default': 100,
                'type': 'int',
                'description': 'Требует баланса с learning_rate (100 по умолчанию)'
            },
            {
                'key': 'learning_rate',
                'label': 'Скорость обучения',
                'default': 0.1,
                'type': 'float',
                'description': 'Меньшие значения = больше деревьев (0.1 по умолчанию)'
            },
            {
                'key': 'max_depth',
                'label': 'Макс. глубина',
                'default': 3,
                'type': 'int',
                'description': 'Обычно 3-5 для текстовых данных (3 по умолчанию)'
            }
        ]
    }
}



VECTORIZERS_SCHEME = {
    'TfIdfVectorizer': {
        'class': TfIdfVectorizer,
        'label': 'TfIdfVectorizer',
        'args': [
            {
                'key': 'stop_words_presets',
                'type': 'multiselect',
                'label': 'Наборы стоп-слов',
                'default': None,
                'variants': [
                    'punct',
                    'num',
                    'prepositions',
                    'conjunctions',
                    'pronouns',
                    'particles'
                ]
            }
        ]
    },
    'BagOfWordsVectorizer': {
        'class': BagOfWordsVectorizer,
        'label': 'BagOfWordsVectorizer',
        'args': [
            {
                'key': 'stop_words_presets',
                'type': 'multiselect',
                'label': 'Наборы стоп-слов',
                'default': None,
                'variants': [
                    'punct',
                    'num',
                    'prepositions',
                    'conjunctions',
                    'pronouns',
                    'particles'
                ]
            }
        ]
    },
    'FastTextVectorizer': {
        'class': FastTextVectorizer,
        'label': 'FastTextVectorizer',
        'args': [
            {
                'key': 'stop_words_presets',
                'type': 'multiselect',
                'label': 'Наборы стоп-слов',
                'default': None,
                'variants': [
                    'punct',
                    'num',
                    'prepositions',
                    'conjunctions',
                    'pronouns',
                    'particles'
                ]
            }
        ]
    },
}
