from sklearn import preprocessing
from sklearn.base import TransformerMixin


class LabelEncoder(TransformerMixin):
    """Handle column_transformer scheme."""

    def __init__(self, *args, **kwargs):
        self.encoder = preprocessing.LabelEncoder(*args, **kwargs)

    def fit(self, X, y=None):
        self.encoder.fit(X)
        return self

    def transform(self, X, y=None):
        return self.encoder.transform(X)

    def inverse_transform(self, X, y=None):
        return self.encoder.inverse_transform(X)
