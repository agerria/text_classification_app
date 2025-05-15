from.base import BaseClassifier

from collections import Counter

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import pairwise_distances

import numpy as np


class KNNClassifier(BaseClassifier):
    def __init__(self, neighbors_count, metric='euclidean'):
        super().__init__()

        self.neighbors_count = neighbors_count
        self.classifier = KNeighborsClassifier(n_neighbors=neighbors_count, metric=metric)

    def fit(self, vectorized_texts, classes):
        self.classifier.fit(vectorized_texts, classes)

    def predict(self, vectorized_texts):
        return self.classifier.predict(vectorized_texts)


class MyKNNClassifier(BaseClassifier):
    def __init__(self, neighbors_count, metric='euclidean'):
        super().__init__()

        self.neighbors_count = neighbors_count
        self.metric = metric
        self.texts_train = None
        self.classes_train = None

    def fit(self, vectorized_texts, classes):
        self.texts_train = vectorized_texts
        self.classes_train = classes

    def predict(self, vectorized_texts):
        distances = pairwise_distances(vectorized_texts, self.texts_train, self.metric)
        neighbors_indices = np.argsort(distances, axis=1)[:, :self.neighbors_count]
        # print('type: ', type(self.classes_train))
        neighbors_labels = self.classes_train[neighbors_indices]
        most_common_labels = [Counter(labels).most_common(1)[0][0] for labels in neighbors_labels]

        return np.array(most_common_labels)
