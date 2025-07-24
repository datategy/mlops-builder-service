from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ArtefactFeaturesStatsNumerical(BaseModel):
    minimum: float
    maximum: float
    mean: float
    std: float
    value_at_percentiles: dict[float, float]


class ArtefactFeaturesStatsText(BaseModel):
    character_length: ArtefactFeaturesStatsNumerical


ArtefactFeaturesStatsDatetime = ArtefactFeaturesStatsNumerical


class ArtefactFeaturesStatsCategoricalTopCategories(BaseModel):
    category: str | int | float | datetime | Any
    """The category name or value."""
    proportion_percentage: float


class ArtefactFeaturesStatsCategorical(BaseModel):
    number_of_unique_values: int
    top_categories: list[ArtefactFeaturesStatsCategoricalTopCategories]


AllStatsT = (
    ArtefactFeaturesStatsCategorical
    | ArtefactFeaturesStatsDatetime
    | ArtefactFeaturesStatsNumerical
    | ArtefactFeaturesStatsText
)
