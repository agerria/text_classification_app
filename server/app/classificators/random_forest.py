from .base import BaseClassifier

from sklearn.ensemble import RandomForestClassifier

class RFClassifier(BaseClassifier):
    def __init__(self, n_estimators=100, max_depth=None, max_features='sqrt'):
        super().__init__()
        self.classifier = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            max_features=max_features,
            class_weight='balanced',  # Часто нужно для текстов
            random_state=42
        )

    def fit(self, vectorized_texts, classes):
        self.classifier.fit(vectorized_texts, classes)

    def predict(self, vectorized_texts):
        return self.classifier.predict(vectorized_texts)
