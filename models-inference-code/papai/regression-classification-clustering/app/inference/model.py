import os
from typing import TYPE_CHECKING

import joblib
import numpy as np

if TYPE_CHECKING:
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
        self.model_path = os.environ.get("MODEL_PATH")
        self.model = self.load_model()

    def load_model(self):
        """Load the model from disk."""
        with open(self.model_path, "rb") as f:
            return joblib.load(f)

    def predict(
        self, features: "TabularMLData"
    ) -> (
        "ClusteringPrediction"
        | "RegressionPrediction"
        | "MultiOutputRegressionPrediction"
        | "MultiClassificationPrediction"
        | "BinaryClassificationPrediction"
    ):
        """Make a prediction using the loaded model."""
        predictions = self.model.predict(features)

        if isinstance(predictions, np.ndarray):
            return predictions.tolist()

        return predictions


# Initialize model
model = MLModel()
