from.base import BaseClassifier

from sklearn.svm import SVC


class SVMClassifier(BaseClassifier):
    def __init__(self, C=1.0, kernel='rbf', random_state=None):
        super().__init__()

        self.kernel = kernel
        self.C = C
        self.classifier = SVC(kernel=self.kernel, C=self.C, random_state=random_state)

    def fit(self, vectorized_texts, classes):
        self.classifier.fit(vectorized_texts, classes)

    def predict(self, vectorized_texts):
        return self.classifier.predict(vectorized_texts)
