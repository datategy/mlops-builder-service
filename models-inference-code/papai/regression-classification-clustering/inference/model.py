import os

import joblib
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.pipeline import make_pipeline

from inference.prediction_types import (
    BinaryClassificationPrediction,
    ClusteringPrediction,
    MultiClassificationPrediction,
    MultiOutputRegressionPrediction,
    RegressionPrediction,
    TabularMLData,
)


class MLModel:
    def __init__(self):
        self.model = None
        self.model_path = os.environ.get("MODEL_PATH", "model.pkl")
        self.load_model()

    def load_model(self):
        """Load the model from disk."""
        with open(self.model_path, "rb") as f:
            self.model_info = joblib.load(f)
        preprocessing = self.model_info.get("preprocessing")
        pca = self.model_info.get("pca")
        poly_tr = self.model_info.get("poly_tr")
        model = self.model_info.get("model")

        non_none_steps: list[BaseEstimator] = []
        for transformer in [preprocessing, pca, poly_tr]:
            if transformer is not None:
                non_none_steps.append(transformer)
        non_none_steps.append(model)

        self.model = make_pipeline(*non_none_steps)

    def predict(
        self, features: TabularMLData
    ) -> (
        ClusteringPrediction
        | RegressionPrediction
        | MultiOutputRegressionPrediction
        | MultiClassificationPrediction
        | BinaryClassificationPrediction
    ):
        """Make a prediction using the loaded model."""
        if self.model is None:
            raise ValueError("Model not loaded")

        predictions = self.model.predict(features)

        if isinstance(predictions, np.ndarray):
            return predictions.tolist()

        return predictions


# Initialize model
model = MLModel()
