import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline


@pytest.fixture
def features() -> list[str]:
    return ["feature1", "feature2", "feature3"]


@pytest.fixture
def model(features) -> Pipeline:
    from sklearn.compose import ColumnTransformer
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler

    std_scaled_features = features[:2]
    return Pipeline(
        steps=[
            (
                "preprocessor",
                ColumnTransformer(
                    transformers=[("num", StandardScaler(), std_scaled_features)],
                    remainder="passthrough",
                ),
            ),
            ("regressor", LinearRegression()),
        ]
    )


@pytest.fixture
def data(features: list[str]) -> tuple[pd.DataFrame, np.ndarray]:
    from sklearn.datasets import make_regression

    n_features = len(features)
    n_informatives = n_features - 1
    X, y = make_regression(n_features=n_features, n_informative=n_informatives, random_state=42)
    X = pd.DataFrame(X, columns=features)
    return X, y


@pytest.fixture
def trained_model(model: Pipeline, data: pd.DataFrame):
    X, y = data
    model.fit(X, y)
    return model


@pytest.fixture
def use_model(trained_model: Pipeline):
    import os

    import joblib

    os.environ["MODEL_PATH"] = "model.joblib"
    joblib.dump(trained_model, "model.joblib")
    yield
    os.remove("model.joblib")


def test_predict_endpoint(use_model):
    from app import predict

    data = {"feature1": [1.0], "feature2": [2.0], "feature3": [3.0]}

    predictions = predict(data)

    assert len(predictions) == 1
    assert isinstance(predictions[0], float)
