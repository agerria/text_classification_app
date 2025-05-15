from .base import BaseVertorizer

from sklearn.feature_extraction.text import TfidfVectorizer as _Vectorizer

class TfIdfVectorizer(BaseVertorizer):
    def __init__(self, stop_words_presets=None):
        super().__init__(stop_words_presets)

        self.vectorizer = _Vectorizer(stop_words=self.stop_words)

    def fit_transform(self, texts):
        return self.vectorizer.fit_transform(texts)