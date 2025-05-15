from.base import BaseClassifier

from sklearn.tree import DecisionTreeClassifier

class DTClassifier(BaseClassifier):
    def __init__(self):
        super().__init__()

        self.classifier = DecisionTreeClassifier()

    def fit(self, vectorized_texts, classes):
        self.classifier.fit(vectorized_texts, classes)

    def predict(self, vectorized_texts):
        return self.classifier.predict(vectorized_texts)
