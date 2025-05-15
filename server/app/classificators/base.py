from scipy.sparse import spmatrix

class BaseClassifier:

    def fit(self, vectorized_texts: spmatrix, classes: list):
        raise NotImplemented

    def predict(self, vectorized_texts: spmatrix) -> list:
        raise NotImplemented
    