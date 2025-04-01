import logging

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger("papai")


class CountVectorizerTransformer(TransformerMixin, BaseEstimator):
    def __init__(self, stop_words=None, max_df=1.0, min_df=1, max_features=None):
        self.stop_words = stop_words
        self.max_df = max_df
        self.min_df = min_df
        self.max_features = max_features
        self.count_vectoriser = CountVectorizer(
            stop_words=self.stop_words,
            max_df=self.max_df,
            min_df=self.min_df,
            max_features=self.max_features,
        )
        self.scaler = MinMaxScaler()
        self.feature_names_in_: str | None = None

    def fit(self, input_features: pd.DataFrame, *_):
        input_feature = extract_process_first_column(input_features)

        self.feature_names_in_ = input_feature.name

        feature_vectorized = self.count_vectoriser.fit_transform(input_feature).toarray()
        self.scaler.fit(feature_vectorized)
        return self

    def transform(self, input_features: pd.DataFrame, *_):
        input_feature = extract_process_first_column(input_features)

        feature_vectorized = self.count_vectoriser.transform(input_feature).toarray()
        return self.scaler.transform(feature_vectorized)

    def fit_transform(self, input_features: pd.DataFrame, *_):
        input_feature = extract_process_first_column(input_features)

        self.feature_names_in_ = input_feature.name

        feature_vectorized = self.count_vectoriser.fit_transform(input_feature).toarray()
        return self.scaler.fit_transform(feature_vectorized)

    def inverse_transform_custom(self, transformed_features, word: str | None = None):
        if word is not None:
            feature_index = np.nonzero(self.get_feature_names_out() == word)
            return (
                transformed_features * self.scaler.data_range_[feature_index]
                + self.scaler.data_min_[feature_index]
            )
        else:
            unscaled_feature = self.scaler.inverse_transform(transformed_features)
            return self.count_vectoriser.inverse_transform(unscaled_feature)

    def get_feature_names_out(self, names: list[str] | None = None):
        if names is not None:
            name = names[0]
        else:
            if self.feature_names_in_ is None:
                raise ValueError("CountVectorizerTransformer is not fit.")
            name = self.feature_names_in_
        return name + "_" + self.count_vectoriser.get_feature_names_out()

    @property
    def vocabulary_(self):
        return self.count_vectoriser.vocabulary_

    @property
    def stop_words_(self):
        return self.count_vectoriser.stop_words_


class TfidfVectorizerCustom(TransformerMixin, BaseEstimator):
    def __init__(self, stop_words=None, max_df=1.0, min_df=1, max_features=None):
        self.stop_words = stop_words
        self.max_df = max_df
        self.min_df = min_df
        self.max_features = max_features
        self.count_vectoriser = CountVectorizer(
            stop_words=self.stop_words,
            max_df=self.max_df,
            min_df=self.min_df,
            max_features=self.max_features,
        )
        self.tfidf_transformer = TfidfTransformer(norm=None)
        self.scaler = MinMaxScaler()
        self.feature_names_in_: str | None = None

    def fit(self, input_features: pd.DataFrame, *_):
        input_feature = extract_process_first_column(input_features)

        self.feature_names_in_ = input_feature.name

        feature_vectorized = self.count_vectoriser.fit_transform(input_feature).toarray()
        tfidf_vectorized = self.tfidf_transformer.fit_transform(feature_vectorized)
        self.scaler.fit(tfidf_vectorized)
        return self

    def transform(self, input_features: pd.DataFrame, *_):
        input_feature = extract_process_first_column(input_features)

        feature_vectorized = self.count_vectoriser.transform(input_feature).toarray()
        tfidf_vectorized = self.tfidf_transformer.transform(feature_vectorized).toarray()
        return self.scaler.transform(tfidf_vectorized)

    def fit_transform(self, input_features: pd.DataFrame, *_):
        input_feature = extract_process_first_column(input_features)

        self.feature_names_in_ = input_feature.name

        feature_vectorized = self.count_vectoriser.fit_transform(input_feature).toarray()
        tfidf_vectorized = self.tfidf_transformer.fit_transform(feature_vectorized).toarray()
        return self.scaler.fit_transform(tfidf_vectorized)

    def inverse_transform_custom(self, transformed_features, word: str | None = None):
        feature_index = np.nonzero(self.get_feature_names_out() == word)
        unnormalized = (
            transformed_features * self.scaler.data_range_[feature_index]
            + self.scaler.data_min_[feature_index]
        )
        return unnormalized / self.tfidf_transformer.idf_[feature_index]

    def get_feature_names_out(self, names: list[str] | None = None):
        if names is not None:
            name = names[0]
        else:
            if self.feature_names_in_ is None:
                raise ValueError("CountVectorizerTransformer is not fit.")
            name = self.feature_names_in_
        return name + "_" + self.count_vectoriser.get_feature_names_out()

    @property
    def vocabulary_(self):
        return self.count_vectoriser.vocabulary_

    @property
    def stop_words_(self):
        return self.count_vectoriser.stop_words_


def extract_process_first_column(input_features: pd.DataFrame) -> pd.Series:
    """Gets the first colonne of a DataFrame and returns it as a Series."""
    return input_features.iloc[:, 0]
