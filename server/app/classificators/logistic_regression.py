from .base import BaseClassifier

from sklearn.linear_model import LogisticRegression


class LRClassifier(BaseClassifier):
    def __init__(self, C=1.0, penalty='l2', class_weight=None):
        super().__init__()
        self.classifier = LogisticRegression(
            C=C,
            penalty=penalty,
            class_weight=class_weight,
            solver='liblinear' if penalty == 'l1' else 'lbfgs',  # Автовыбор solver
            max_iter=1000  # Увеличение для сходимости на текстах
        )

    def fit(self, vectorized_texts, classes):
        self.classifier.fit(vectorized_texts, classes)

    def predict(self, vectorized_texts):
        return self.classifier.predict(vectorized_texts)
