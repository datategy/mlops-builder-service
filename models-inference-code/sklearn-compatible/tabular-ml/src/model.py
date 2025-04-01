import os

import joblib
import numpy as np

from .prediction_types import (
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
            self.model = joblib.load(f)

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
