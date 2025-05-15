from .base import BaseClassifier

from sklearn.ensemble import GradientBoostingClassifier


class GBClassifier(BaseClassifier):
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3):
        super().__init__()
        self.classifier = GradientBoostingClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            max_features='log2',  # Оптимально для текстовых данных
            random_state=42
        )

    def fit(self, vectorized_texts, classes):
        self.classifier.fit(vectorized_texts, classes)

    def predict(self, vectorized_texts):
        return self.classifier.predict(vectorized_texts)
