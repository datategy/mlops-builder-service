from typing import Annotated, Literal, TypedDict

import pandas as pd
from fastapi import Body, FastAPI
from pydantic import BaseModel

from inference.model import model
from inference.prediction_types import (
    BinaryClassificationPrediction,
    ClusteringPrediction,
    MultiClassificationPrediction,
    MultiOutputRegressionPrediction,
    RegressionPrediction,
    TabularMLData,
)

app = FastAPI(title="Model API", description="API for model inference")


class HealthCheckResponse(BaseModel):
    status: Literal["healthy", "unhealthy"]
    status_message: str | None = None


@app.get("/health")
def health_check() -> HealthCheckResponse:
    if model.model is None:
        return HealthCheckResponse(status="unhealthy", status_message="Model not loaded")

    return HealthCheckResponse(status="healthy")


class InputData(TypedDict):
    features: TabularMLData


@app.post("/predict")
def predict(
    data: Annotated[InputData, Body()],
) -> (
    ClusteringPrediction
    | RegressionPrediction
    | MultiOutputRegressionPrediction
    | MultiClassificationPrediction
    | BinaryClassificationPrediction
):
    features = pd.DataFrame(data["features"])
    prediction = model.predict(features)
    return prediction
