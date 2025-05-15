from .base import BaseVertorizer
import numpy as np
import pandas as pd
from scipy.sparse import spmatrix
import pickle
import os
import pymorphy3
from razdel import tokenize


from gensim.models.keyedvectors import KeyedVectors


MODEL_FILE = 'models/cc.ru.300.vec'
DUMP_FILE = f'{MODEL_FILE}.dump'


class FastTextVectorizer(BaseVertorizer):
    def __init__(self, stop_words_presets=None):
        super().__init__(stop_words_presets)
        self.model = self.load_model()
        self.save_model(self.model)
        # self.morph = pymorphy3.MorphAnalyzer()
        # self.tokenizer = (lambda text: [self.morph.parse(token.text)[0].normal_form for token in tokenize(text)])
        self.tokenizer = lambda text: text.lower().replace(',', '').replace('.', '').replace('!', '').replace('?', '').split()

    
    def fit_transform(self, texts: pd.DataFrame) -> spmatrix:
        texts_series = texts
        vectors = []
        for text in texts_series:
            tokens = self.tokenizer(text)
            tokens = [token for token in tokens if token not in self.stop_words]
            word_vectors = []
            for token in tokens:
                if token in self.model:
                    word_vectors.append(self.model[token])
            if word_vectors:
                text_vector = np.mean(word_vectors, axis=0)
            else:
                text_vector = np.zeros(self.model.vector_size)
            vectors.append(text_vector)
        return np.vstack(vectors)
        
    
    def load_model(self):
        if os.path.exists(DUMP_FILE):
            with open(DUMP_FILE, 'rb') as f:
                model = pickle.load(f)
            return model
        return KeyedVectors.load_word2vec_format(MODEL_FILE, binary=False)
    
    def save_model(self, model):
        if not os.path.exists(DUMP_FILE):
            with open(DUMP_FILE, 'wb') as f:
                pickle.dump(model, f)    
    
    
    
    