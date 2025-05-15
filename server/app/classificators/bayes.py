from.base import BaseClassifier

from scipy.sparse import issparse
from sklearn.naive_bayes import MultinomialNB, GaussianNB

import numpy as np


class NBClassifier(BaseClassifier):
    def __init__(self, alpha=1.0):
        super().__init__()

        self.alpha = alpha
        self.classifier = MultinomialNB(alpha=self.alpha)
        # self.classifier = GaussianNB()

    def fit(self, vectorized_texts, classes):
        self.classifier.fit(vectorized_texts, classes)

    def predict(self, vectorized_texts):
        return self.classifier.predict(vectorized_texts)


class MyNBClassifier(BaseClassifier):
    def __init__(self, alpha=1.0):
        super().__init__()

        self.alpha = alpha
        self.class_log_prior = None
        self.feature_log_prob = None
        self.uniq_classes = None

    def fit(self, vectorized_texts, classes):
        if issparse(vectorized_texts):
            vectorized_texts = vectorized_texts.tocsc()

        self.uniq_classes = np.unique(classes)
        n_classes = len(self.uniq_classes)

        class_count = np.array([np.sum(classes == c) for c in self.uniq_classes])
        self.class_log_prior = np.log(class_count) - np.log(class_count.sum())

        feature_count = np.zeros((n_classes, vectorized_texts.shape[1]), dtype=np.float64)

        for i, c in enumerate(self.uniq_classes):
            X_c = vectorized_texts[classes == c]
            feature_count[i, :] = X_c.sum(axis=0)

        smoothed_fc = feature_count + self.alpha
        smoothed_cc = smoothed_fc.sum(axis=1).reshape(-1, 1)
        self.feature_log_prob = np.log(smoothed_fc) - np.log(smoothed_cc)

    def predict(self, vectorized_texts):
        if issparse(vectorized_texts):
            vectorized_texts = vectorized_texts.tocsc()

        jll = (vectorized_texts @ self.feature_log_prob.T) + self.class_log_prior
        return self.uniq_classes[np.argmax(jll, axis=1)]
